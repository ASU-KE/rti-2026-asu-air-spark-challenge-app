# API Implementation Patterns

Handlers implementing the conventions in [`SKILL.md`](SKILL.md): schema validation, `422` on validation failure, `201` with a `Location` header on create, and the `{ data }` / `{ error }` envelope. FastAPI (Pydantic v2) is the backend vehicle; the TypeScript block is the React client that consumes it. Reach for the block matching your side of the stack.

## Python (FastAPI + Pydantic v2)

```python
from datetime import datetime

from fastapi import APIRouter, FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/api/v1")


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)


class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime


class UserEnvelope(BaseModel):
    data: User


@router.post(
    "/users",
    response_model=UserEnvelope,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: CreateUserRequest, response: Response) -> UserEnvelope:
    # FastAPI validates `payload` against the model and returns 422 on failure.
    user = await user_service.create(email=payload.email, name=payload.name)
    response.headers["Location"] = f"/api/v1/users/{user.id}"
    return UserEnvelope(data=user)


# Reshape validation failures into the documented { error } envelope.
async def on_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": [
                    {
                        "field": ".".join(str(p) for p in err["loc"] if p != "body"),
                        "message": err["msg"],
                        "code": err["type"],
                    }
                    for err in exc.errors()
                ],
            }
        },
    )


app = FastAPI()
app.add_exception_handler(RequestValidationError, on_validation_error)
app.include_router(router)
```

## TypeScript (React API client)

```typescript
import { z } from "zod";

// Mirror the response contract as client-side types, then parse at the boundary.
const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  name: z.string(),
  created_at: z.string().datetime(),
});

const userEnvelopeSchema = z.object({ data: userSchema });

const apiErrorSchema = z.object({
  error: z.object({
    code: z.string(),
    message: z.string(),
    details: z
      .array(
        z.object({ field: z.string(), message: z.string(), code: z.string() }),
      )
      .optional(),
  }),
});

export type User = z.infer<typeof userSchema>;

export interface CreateUserInput {
  email: string;
  name: string;
}

export class ApiValidationError extends Error {
  constructor(
    message: string,
    readonly details: { field: string; message: string; code: string }[],
  ) {
    super(message);
    this.name = "ApiValidationError";
  }
}

export async function createUser(input: CreateUserInput): Promise<User> {
  const res = await fetch("/api/v1/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });

  if (res.status === 422) {
    const { error } = apiErrorSchema.parse(await res.json());
    throw new ApiValidationError(error.message, error.details ?? []);
  }
  if (!res.ok) {
    throw new Error(`Request failed with status ${res.status}`);
  }

  const { data } = userEnvelopeSchema.parse(await res.json());
  return data;
}
```

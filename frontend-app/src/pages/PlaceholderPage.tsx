interface PlaceholderPageProps {
  title: string;
  description: string;
}

/**
 * Shared stub for the four screens in the scaffold. Each screen renders a
 * single `h1` (the app's per-page landmark heading) and a short description of
 * the behavior a later slice will build here.
 */
export function PlaceholderPage({ title, description }: PlaceholderPageProps) {
  return (
    <article className="page-placeholder">
      <h1>{title}</h1>
      <p>{description}</p>
      <p className="page-placeholder__status" role="note">
        This screen is a scaffold placeholder. Its behavior arrives in a later
        slice.
      </p>
    </article>
  );
}

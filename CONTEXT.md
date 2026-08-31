# RTI ASU AIR Spark Challenge

This context defines the shared language for the RTI challenge team’s application delivery and agent-centric software development lifecycle experiment.

## Project Outcomes

**Challenge Application**:
The AI-powered application prototype submitted to and demonstrated at the ASU AIR Spark Challenge. It owns the event critical path when application delivery and process experimentation conflict.
_Avoid_: Test app, throwaway app, workflow demo

**aSDLC Pilot**:
The instrumented trial of an agent-centric software development lifecycle used to deliver the Challenge Application. It produces evidence, limitations, lessons, and a standards backlog rather than a claim of production readiness.
_Avoid_: Enterprise-ready aSDLC, finalized RTO standard

**Enterprise-Informed**:
Designed with ASU and Knowledge Enterprise expectations for security, reliability, traceability, maintainability, and human accountability in view, without claiming those qualities have been fully validated for mission-critical production use.
_Avoid_: Enterprise-ready, production-proven

**Event Critical Path**:
The minimum sequence of work required to produce a valid submission and credible live demonstration by the challenge deadlines. It takes precedence over optional aSDLC experiments.
_Avoid_: Full project roadmap

## Concept Selection

**Primary Concept**:
The application concept selected as the team’s intended Challenge Application after structured scoring.
_Avoid_: Favorite idea, final product

**Fallback Concept**:
A reduced-risk alternative that the team can deliver if the Primary Concept becomes infeasible within the event constraints.
_Avoid_: Secondary feature, stretch goal

## Team Roles

**Challenge Lead and Mentor**:
Nathan Rollins’s facilitation role for coordination, mentoring, and protecting the event critical path; it does not grant unilateral authority over co-equal product or implementation decisions.
_Avoid_: Product owner, sole decision maker

**Challenge Team Member**:
Nathan Rollins, Rajashree Pailla, or Vinay Veeramallu acting as a co-equal participant in team decisions, implementation, and review.
_Avoid_: Subordinate, assigned developer

**Presenter**:
The team member selected through team discussion before the event to lead the live pitch and demonstration, with the other members supporting preparation and jury questions.
_Avoid_: Challenge Lead

## Human-Agent Collaboration

**Human-Agent Pair Programming**:
An extension of pair programming in which a human remains accountable while one or more AI agents perform bounded research, design, implementation, testing, review, or documentation work under approved scope and authority.
_Avoid_: Human-Agent Partnership, Developer-Agent PPP, agent-led development

**Interactive Pairing**:
A Human-Agent Pair Programming mode in which the human and agent collaborate synchronously throughout the work.
_Avoid_: Live agent session

**Delegated Pairing**:
A Human-Agent Pair Programming mode in which an agent executes an approved, bounded ticket asynchronously while a named human partner remains accountable for scope, checkpoints, and acceptance.
_Avoid_: Unsupervised agent work, AFK autonomy

**Autonomous Work**:
Read-only investigation, approved-source research, drafting, and non-mutating validation that an agent may perform without repeated authorization.
_Avoid_: Unsupervised delivery

**Ticket-Authorized Work**:
Reversible delivery work an agent may perform after assignment to an approved ticket, including editing files, running tests, creating a branch, committing, and opening or updating a pull request.
_Avoid_: Unbounded autonomy, implied production authority

**Human-Gated Action**:
An action requiring explicit human approval because it changes shared or live state, accepts risk, uses elevated credentials, exceeds approved scope, or may be destructive.
_Avoid_: Routine agent action

## Delivery Workflow

**Standard Lane**:
The normal delivery path from approved issue through claim, implementation and testing, independent review, pull request, human approval, and merge.
_Avoid_: Full lane, slow lane

**Event-Critical Lane**:
A documented reduced-ceremony path approved by the Challenge Lead and Mentor to protect the Event Critical Path. It retains acceptance criteria, targeted validation, the same integrated review skills used by the Standard Lane, human merge approval, and non-bypassable security controls.
_Avoid_: Shortcut, bypass, hotfix lane

**Definition of Ready**:
The minimum information and risk screening an issue must contain before it can be claimed: outcome, acceptance criteria, test seam, dependencies, affected interfaces, risk, pairing mode, accountable human, and reviewable scope.
_Avoid_: Open issue, untriaged request

**Definition of Done**:
The state reached when acceptance and validation evidence, mandatory reviews, independent human approval, merge, pairing evidence, and required follow-up records are complete.
_Avoid_: Code complete, agent finished

## Assurance and Skill Adaptation

**Integrated Code Review**:
The single review entry point applied to every pull request, combining specification conformance, repository standards, pull-request quality and risk, mandatory security review, independent cross-model review, cross-validation, and one synthesized merge recommendation.
_Avoid_: Optional adversarial review, lane-specific review, review menu

**Universal Security Baseline**:
Security controls evaluated for every pull request regardless of application platform, including secrets, access control, sensitive data, dependencies, injection, logging, network exposure, abuse resistance, least privilege, and AI-specific threats.
_Avoid_: AWS-only security review, optional security pass

**Provider Layer**:
Conditional security and reliability controls for the application’s deployment platform. Google Cloud and Google Kubernetes Engine are required provider layers for the Challenge Application; other providers remain optional overlays when relevant.
_Avoid_: Universal baseline, cloud-neutral control

**Adapted Skill**:
A copied skill modified in place for the RTI challenge workflow while retaining explicit provenance to its upstream repository, source path, pinned revision, import date, and local behavior changes.
_Avoid_: Pristine upstream skill, RTO-owned original

**Session Evidence Record**:
A structured, redacted summary of one Human-Agent Pair Programming session linked to its primary ticket and related pull request, recording mode, scope, effort, validation, review, failures, interventions, deviations, and outcome.
_Avoid_: Raw transcript, prompt archive, activity log

**Standards Backlog**:
Post-pilot work needed to evaluate, revise, or validate aSDLC practices before they can become an RTO standard.
_Avoid_: Final standard, accepted policy

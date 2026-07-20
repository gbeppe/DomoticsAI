# DomoticsAI Governance Toolkit — Execution Framework

## Purpose

The execution framework defines how DomoticsAI Governance Toolkit commands
change their operational behaviour according to the selected execution mode.

It separates:

- the execution mode selected by the caller;
- the policies associated with that mode;
- the execution context passed to governance tools;
- the command-specific work performed by the processing pipeline.

The framework is intended to centralize execution behaviour and prevent
individual governance tools from implementing their own mode-specific logic.

## Architectural flow

```text
Command-line arguments
        |
        v
ExecutionMode
        |
        v
ExecutionPolicy.from_mode()
        |
        v
ExecutionContext
        |
        v
Governance command
        |
        v
Processing pipeline

The command-line interface is responsible for interpreting external input and
constructing the execution framework objects.

Governance tools receive the resulting ExecutionContext and must not
reconstruct an ExecutionMode or an ExecutionPolicy.

ExecutionMode

ExecutionMode identifies the execution profile requested by the caller.

Supported values are:

Mode	Purpose
generate	Produce governance reports without failing because of findings
check	Evaluate the repository and fail when significant findings exist
ci	Apply automated-check behaviour with verbose output enabled

ExecutionMode contains only mode identity and input normalization. It does
not implement report, finding, or exit-code behaviour.

String values are resolved through:

ExecutionMode.from_value(value)
ExecutionPolicy

ExecutionPolicy is the centralized representation of the behaviour associated
with an ExecutionMode.

It contains:

generate_reports;
finding_policy;
verbose_output;
exit_policy.

Policies are resolved through:

ExecutionPolicy.from_mode(mode)

This method is the authoritative mapping between execution modes and execution
behaviour.

Governance commands must consume the resolved policy rather than branch
directly on ExecutionMode.

Policy matrix
Mode	Generate reports	Finding threshold	Verbose output	Exit strategy
generate	Yes	none	No	success
check	No	low	No	fail_on_findings
ci	No	low	Yes	fail_on_findings

The matrix describes the current behaviour of the framework. Changes to this
matrix are behavioural changes and require dedicated tests and an explicit work
package.

FindingPolicy

FindingPolicy defines the minimum severity considered significant during an
execution.

Supported thresholds are:

Threshold	Meaning
none	Findings do not cause execution failure
low	Low, medium, and high findings are significant
medium	Medium and high findings are significant
high	Only high findings are significant

The policy stores the configured threshold. Command integration is responsible
for evaluating command results against that threshold.

ExitPolicy

ExitPolicy defines how the presence of significant findings affects the
process exit code.

Supported strategies are:

Strategy	Behaviour
success	Always return exit code 0
fail_on_findings	Return exit code 3 when significant findings exist

The decision is applied through:

policy.exit_policy.exit_code(has_findings)

The CLI determines whether significant findings exist, while ExitPolicy
determines the corresponding process exit code.

This separation prevents command-line code from reimplementing exit-strategy
behaviour.

ExecutionContext

ExecutionContext carries the immutable execution inputs required by governance
tools:

repository root;
governance package root;
loaded configuration;
execution mode;
resolved execution policy.

The context is built through:

build_context(
    repository_root,
    configuration,
    execution_mode,
    execution_policy,
)

When no explicit policy is supplied, build_context resolves it from the
execution mode.

Allowing an explicit policy supports testing and controlled integration without
requiring governance tools to construct policies themselves.

Command-line responsibilities

The governance CLI owns the boundary between user input and internal execution
objects.

Its responsibilities are:

parse command-line arguments;
normalize the requested ExecutionMode;
resolve the corresponding ExecutionPolicy;
construct the ExecutionContext;
invoke the selected governance command;
apply command-specific overrides;
emit the command result and process exit code.

The CLI may consume policy values, but it must not duplicate the mode-to-policy
matrix.

Repository Census integration

Repository Census receives an ExecutionContext and runs its processing
pipeline:

ScanStage
    |
    v
RuleStage
    |
    v
StatisticsStage
    |
    v
InventoryStage

The Census engine and its stages do not interpret ExecutionMode and do not
construct execution policies.

The CLI currently applies the execution policy to Census results by:

generating reports when generate_reports is enabled;
selecting the effective finding threshold;
determining whether significant findings exist;
delegating exit-code evaluation to ExitPolicy.

This keeps repository analysis independent from command-line execution
behaviour.

--fail-on override

The Census command supports:

--fail-on none
--fail-on low
--fail-on medium
--fail-on high

When the option is absent, the threshold comes from:

policy.finding_policy.threshold

When the option is present, it becomes the effective threshold for that command
execution.

The override does not mutate ExecutionPolicy or FindingPolicy. Both policy
objects remain immutable.

The override changes only the effective threshold used to evaluate the current
Census result.

Immutability

The following framework objects are immutable dataclasses:

ExecutionPolicy;
FindingPolicy;
ExitPolicy;
ExecutionContext.

Immutability ensures that execution behaviour cannot change while a governance
command or pipeline is running.

Derived values, such as the effective threshold produced by --fail-on, must
be stored separately and must not modify policy instances.

Extension rules

Future governance commands and execution behaviours must follow these rules.

Adding a governance command

A new command must:

receive the existing ExecutionContext;
consume the resolved ExecutionPolicy;
avoid constructing its own policy;
avoid direct branching on ExecutionMode when a policy value can express the
required behaviour.
Adding an execution mode

A new mode requires:

a new stable ExecutionMode value;
an explicit entry in ExecutionPolicy.from_mode;
unit tests for the complete policy mapping;
CLI integration tests;
regression tests for every affected governance command;
an update to the policy matrix in this document.
Adding policy behaviour

New execution behaviour should be represented by a dedicated policy value or a
small immutable policy object when it has an independent responsibility.

Policy objects should describe or apply execution behaviour. They must not
perform repository scanning, file-system discovery, report rendering, or other
domain processing.

Command-specific overrides

An override must:

be explicit in the command interface;
apply only to the current execution;
leave the original policy immutable;
be covered by tests for both default and overridden behaviour.
Architectural invariants

The execution framework must preserve the following invariants:

ExecutionMode identifies a profile but does not implement its behaviour.
ExecutionPolicy.from_mode is the authoritative mode-to-policy mapping.
The CLI constructs the execution mode, policy, and context.
Governance tools consume ExecutionContext.
Repository Census does not reconstruct or interpret execution modes.
Policy objects remain immutable during execution.
Command-specific overrides do not mutate policy objects.
Report generation follows ExecutionPolicy.generate_reports.
Finding significance follows the effective finding threshold.
Exit-code behaviour is delegated to ExitPolicy.

Changes that violate these invariants require an explicit architectural review.

Current verification coverage

The framework is covered by dedicated tests for:

execution-mode values and parsing;
execution-policy mapping and immutability;
finding thresholds and immutability;
exit strategies, exit-code evaluation, and immutability;
execution-context defaults and explicit policy injection;
CLI context construction;
report generation for each execution mode;
default finding thresholds;
--fail-on overrides;
Repository Census pipeline stages;
processing-pipeline sequencing.

These tests define the observable behaviour that consolidation changes must
preserve.

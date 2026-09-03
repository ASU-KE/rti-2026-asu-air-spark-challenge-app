# Application Requirements for AIRgents of Change

Application title: AIRgents of Change

This is a full-stack application that will operate as a lightweight multi-agent harness. It will allow a researcher to organize groups of LLM agents to perform experiments on problems of social collective action when agents have differential access to information and communication. It must support OpenAI-compatible LLM providers.

The prototype will run locally on development workstations only. Cloud deployment (GCP or otherwise) is out of scope for the prototype; actual deployment and hosting architecture may be planned separately at a later time.

The frontend application will be a Typescript React, and the backend will be Python FastAPI.

This will be a flexible framework for creating structured context, organized into access layers or shells, and groups of agents working to achieve pre-defined goals. An orchestrator agent, possibly operating with deterministic scripts, will be responsible for monitoring and testing the outcomes of the agents' work to determine when project-specified end-states have been achieved and the run is to be terminated. Structured dataset inputs will be required as an initial starting point, upon which the tasked agents will interact and produce documented work output that can be collected and analyzed afterward.

Agents will be organized into configurable networks. Network topology and density must be configurable at multiple-scales: network-wide, role groupings, and individuals.

Agents can be organized along multiple axes of differentiation:

1. Role-based goals
2. Persona behaviors
3. Network-structural variations that determine access to context information and inter-agent-communications

The key goal for this application is flexibility in configuration. It must be capable of supporting large numbers of agents (10 during prototype phase, and the capability to expand in future, 50+), while responsibly using the LLM provider through request rate limiting and request queuing.

There will need to be some sort of time-control or sequencing system to allow the researcher to configure synchronous and asynchronous decisions and communications.

The frontend dashboard should allow the researcher to organize the agents into networks, assign the agents to custom roles and personas, and assign custom instructions and goals. Network relationships need to be highly customizable, but also support common presets, such as no-connections, pair-couple, small-world, and so on.

The dashboard should provide a nice overview of the network relationships, how information access is organized and restricted, and to be able to easily identify role groups and personas.

Initial data sets must easy to manage and to map to the agents. Agent actions will result in intermediate datasets, which need to be observable. And the final dataset at the end of the run must be viewable and exportable.

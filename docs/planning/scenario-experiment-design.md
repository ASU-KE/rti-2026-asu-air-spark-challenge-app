This is Criminal Jury Trial where a group of jury member agents must come to a consensus decision: Guilty or Non-Guilty.

- The jury will consist of 6 agents.
- Two small groups (2 each) of attorney agents, the Prosecution and Defense.

The opinions and evidence will be structured along opinion (0-1), strength of that opinion (0-1), and some Value category that is important to the agent. The value will be a text property from a fixed list of values: in principle they could be recognizable values, like "crime", "liberterianism", "mercy", etc. But for this prototype scenario it wil be two options only: "A" or "B"

Agents, attorneys, and evidence will be assigned values along those three properties. We can start with random assignments. A researcher would be able to configure their own assignments as desired. There needs to be a mechanism for importing a set of values, e.g. CSV file.

The Prosecution and Defense teams must attempt to convince the jury to Convict (Guilty = 1) or Acquit (Not-Guilty = 0). Evidence will be provided by the attorneys to share with the jury and attempt to influence their opinions.

Each group of attorneys will have a pool of evidence items available to them with random collection of property values that are advantageous to their goal and disadvantageous to the opposing side. For the prototype 10 evidence items will be assigned to each team with random values assigned.

This means that sharing that evidence item will either increase a jury agent's opinion toward Guilty or lower it toward Non-Guilty (0-1). The influence effect that evidence item has will be a calculated factor composed mathematically as `[opinion-delta: -1 to +1] x [strength of evidence 0-1] and value it is related (A, B).

For a given item of evidence, when a jurist receives that information, it adjusts its opinion based on the final calculated delta factor of the evidence if that item also corresponds with the Value they hold (A,B), and the confdence increases with that same delta. If the values don't match, then there is no effect on the agent's opinion. Reminder: all these values are configurable by the researcher.

A single Experiment consists of multiple Runs, where the outcomes and final outputs from the Round can be collected and analyzed for statistical patterns. Inlcude the final internal states for all agents in the model, and the final verdict consensus from the jurists. Within each Run will be a series of Rounds for the groups as follows:

1. Each attorney group will randomly select one evidence item to communicate to the jurists in order to persuade them.
2. The defense presents their evidence to all jurist.
3. The prosecution presents their evidence to all jurists.

For simplicity, the jury will be networked in a ring, with each agent connected to their two adjacent neighbors.

Each attorney group will have directed connection to all agents in the jurists group.

4. The jurists take turns processing both evidence items from the Defense and Prosecution, in that order. Each agent adjusts its own opinion value and strength based on the evidence metric. For the prototype example: `if evidence type = agent value type, then adjust the opinion and confidence up or down according to the evidence delta factor. Confidence is adjusted by the same opinion delta factor but multiplied by a fixed numeric value 0-1.` (Future tweak to the scenario may be to make Value not a binary but proximty measure. So if the evidence matches the agent's value type, it increases the confidence strength. If the value differs, it reduces confidence.)
5. Each agent takes turns communicating their new opinions and confidence values to their adjacent neighbors.
6. After everyone has communicated to their neighbors, every agent updates their opinion based on the information received from their neighbors. Again, if a neighbor shares the same Value or not, the agent will adjust their opinion up or down based on a mathematical factor TBD).
7. The Round ends.

The Experiment Run will be ended when:

1. The jury agents reach a predetermined minimum variance in their opinion values (aka verdict reached), or
2. They fail to reach consensus once a predefined round limit has been reached (Hung Jury).

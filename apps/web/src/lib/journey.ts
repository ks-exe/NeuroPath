/**
 * Engagement journey, in the order required by R10.8 and described on the
 * How We Work page (R13.4). Shared by the homepage and /how-we-work.
 *
 * COPY FOR FOUNDER REVIEW: the step names come from the spec (R10.8). The
 * `clientProvides` and `neuropathDelivers` text is not given by the spec; it
 * describes the intended process only and makes no claim about timelines,
 * prices, past engagements or results.
 */
export interface JourneyStep {
  readonly name: string;
  readonly clientProvides: string;
  readonly neuropathDelivers: string;
}

export const journeySteps: readonly JourneyStep[] = [
  {
    name: "Discovery",
    clientProvides: "A description of the problem in your own words, and the context around it.",
    neuropathDelivers: "Questions that clarify the problem, and a first view of whether we can help.",
  },
  {
    name: "Requirement Analysis",
    clientProvides: "Answers to our questions, access to the people who know the process, and any existing documents.",
    neuropathDelivers: "A written summary of the requirements for you to review and correct.",
  },
  {
    name: "Solution Architecture",
    clientProvides: "Feedback on constraints such as existing systems, data, and security needs.",
    neuropathDelivers: "A proposed technical approach, explained in plain language.",
  },
  {
    name: "Proposal",
    clientProvides: "Review of the proposal and any questions about it.",
    neuropathDelivers: "A proposal describing scope, deliverables, and how the work will be organised.",
  },
  {
    name: "Agreement",
    clientProvides: "Approval of the agreed scope and terms.",
    neuropathDelivers: "A confirmed agreement before engineering work starts.",
  },
  {
    name: "Engineering",
    clientProvides: "Timely feedback and access to the systems and data the work depends on.",
    neuropathDelivers: "The solution, built against the agreed scope, with progress shared along the way.",
  },
  {
    name: "Testing",
    clientProvides: "Participation in checking that the solution works for your process.",
    neuropathDelivers: "Testing of the solution against the agreed requirements.",
  },
  {
    name: "Deployment",
    clientProvides: "Access to the target environment and approval to go live.",
    neuropathDelivers: "The solution deployed to the agreed environment.",
  },
  {
    name: "Handover",
    clientProvides: "The people who will own and operate the solution.",
    neuropathDelivers: "Documentation and a walkthrough so your team can use and operate the solution.",
  },
  {
    name: "Maintenance",
    clientProvides: "Reports of issues and requests for changes.",
    neuropathDelivers: "Support and maintenance as set out in the agreement.",
  },
];

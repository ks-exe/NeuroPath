import type { ServiceGroup } from "./types";

/** Lawful data collection statement (R12.9). */
export const DATA_COLLECTION_COMPLIANCE_NOTE =
  "Engagements that involve web scraping or automated data collection respect applicable laws, website terms of service, access controls, and privacy requirements.";

/** Service groups A to F and their detail lists, taken from R12.1 to R12.7. */
export const serviceGroups: readonly ServiceGroup[] = [
  {
    id: "A",
    slug: "ai-ml-engineering",
    name: "AI & ML Engineering",
    details: [
      "Custom AI applications",
      "LLM integrations",
      "RAG systems",
      "AI agents and agentic workflows",
      "Intelligent automation",
      "Predictive analytics",
      "Machine learning model development",
      "AI decision support",
      "Model integration and deployment",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
  },
  {
    id: "B",
    slug: "data-engineering-analytics",
    name: "Data Engineering & Analytics",
    details: [
      "Data pipelines",
      "ETL and ELT",
      "Data ingestion and processing",
      "Data warehousing",
      "Data transformation",
      "Data quality engineering",
      "Business intelligence",
      "Analytics dashboards",
      "Data architecture",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
    complianceNote: DATA_COLLECTION_COMPLIANCE_NOTE,
  },
  {
    id: "C",
    slug: "cloud-devops",
    name: "Cloud & DevOps",
    details: [
      "Cloud architecture",
      "AWS infrastructure",
      "Infrastructure as code",
      "CI/CD",
      "Containerization",
      "Deployment",
      "Monitoring and observability",
      "Cloud optimization",
      "Reliability and security engineering",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
  },
  {
    id: "D",
    slug: "custom-software-engineering",
    name: "Custom Software Engineering",
    details: [
      "Custom web applications",
      "Backend systems",
      "APIs",
      "Database architecture",
      "Internal business platforms",
      "Modernization",
      "Third-party integrations",
      "Full-stack development",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
  },
  {
    id: "E",
    slug: "intelligent-automation-integration",
    name: "Intelligent Automation & Integration",
    details: [
      "Workflow automation",
      "Internal operational automation",
      "AI-assisted processes",
      "System-to-system integration",
      "Document processing",
      "Data synchronization",
      "Operational efficiency",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
    complianceNote: DATA_COLLECTION_COMPLIANCE_NOTE,
  },
  {
    id: "F",
    slug: "technical-consulting-architecture",
    name: "Technical Consulting & Architecture",
    details: [
      "Technical discovery",
      "Feasibility analysis",
      "System architecture",
      "Technology selection",
      "Cloud architecture consulting",
      "Technical audits",
      "Project planning",
      "Engineering roadmaps",
    ],
    // FOUNDER INPUT NEEDED (R12.10): the spec gives no wording for these lists.
    engagements: [],
    deliverables: [],
    technologies: [],
  },
];

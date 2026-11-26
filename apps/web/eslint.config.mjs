import { FlatCompat } from "@eslint/eslintrc";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const compat = new FlatCompat({ baseDirectory: dirname(fileURLToPath(import.meta.url)) });

const awsPattern = { group: ["@aws-sdk/*", "aws-sdk"], message: "The Web_App must not use AWS SDKs; call /api/v1 instead." };

const eslintConfig = [
  { ignores: [".next/**", "node_modules/**", "next-env.d.ts"] },
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    // The Web_App must never use AWS SDKs (R2.8).
    rules: {
      "no-restricted-imports": ["error", { patterns: [awsPattern] }],
    },
  },
  {
    // No gradients, no glassmorphism (R4.4). Test files are exempt so they can
    // contain the forbidden class names as fixtures.
    files: ["src/**/*.{ts,tsx,js,jsx,mjs}"],
    ignores: ["**/*.test.{ts,tsx}"],
    rules: {
      "no-restricted-syntax": [
        "error",
        ...[
          "Literal[value=/bg-gradient-/]",
          "Literal[value=/backdrop-blur/]",
          "TemplateElement[value.raw=/bg-gradient-/]",
          "TemplateElement[value.raw=/backdrop-blur/]",
          "JSXText[value=/bg-gradient-/]",
          "JSXText[value=/backdrop-blur/]",
        ].map((selector) => ({
          selector,
          message: "Gradients (bg-gradient-*) and glassmorphism (backdrop-blur) are not allowed (R4.4).",
        })),
      ],
    },
  },
  {
    // Core code must never import a Lab module (R1.4, R55.9). Lab route groups
    // live under src/app/(labs)/ or src/labs/; everything else is core.
    files: ["src/**/*.{ts,tsx,js,jsx,mjs}"],
    ignores: ["src/app/\\(labs\\)/**", "src/app/(labs)/**", "src/labs/**", "**/*.test.{ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            awsPattern,
            {
              group: ["@/labs", "@/labs/*", "**/labs", "**/labs/*", "@/app/(labs)", "@/app/(labs)/*", "**/(labs)", "**/(labs)/*"],
              message: "Core modules must not import Lab modules (R1.4, R55.9).",
            },
          ],
        },
      ],
    },
  },
];

export default eslintConfig;

import { FlatCompat } from "@eslint/eslintrc";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({ baseDirectory: __dirname });

const config = [
  {
    ignores: [".next/**", "node_modules/**", "out/**", "next-env.d.ts"],
  },
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      // The product copy is conversational and leans on contractions
      // ("Today's Vibe", "how you're feeling"). Apostrophes and quotes in
      // JSX text render correctly, so escaping them as entities would only
      // make the copy harder to read and edit.
      "react/no-unescaped-entities": "off",
    },
  },
];

export default config;

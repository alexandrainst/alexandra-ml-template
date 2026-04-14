import vueEslintParser from "vue-eslint-parser";
import js from "@eslint/js";
import pluginVue from "eslint-plugin-vue";
import ts from "@typescript-eslint/parser";
import pluginTs from "@typescript-eslint/eslint-plugin";
import prettier from "eslint-plugin-prettier/recommended";

export default [
  js.configs.recommended,
  ...pluginVue.configs["flat/recommended"],
  {
    files: ["**/*.ts", "**/*.tsx", "**/*.vue"],
    languageOptions: {
      parser: ts,
      parserOptions: {
        extraFileExtensions: [".vue"],
        sourceType: "module",
      },
    },
    plugins: {
      "@typescript-eslint": pluginTs,
    },
    rules: {
      ...pluginTs.configs.recommended.rules,
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },
  {
    files: ["**/*.vue"],
    languageOptions: {
      parser: vueEslintParser,
      parserOptions: {
        parser: ts,
        extraFileExtensions: [".vue"],
        sourceType: "module",
      },
    },
    rules: {
      "vue/multi-word-component-names": "warn",
      "vue/no-unused-vars": "error",
    },
  },
  prettier,
];

import globals from 'globals';
import pluginJs from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginReact from 'eslint-plugin-react';

export default [
  {
    ignores: ['dist', '*.cjs', 'backend/**/*.py', 'logs.json.backup']
  },
  {
    files: ['**/*.{js,mjs,ts,jsx,tsx}'],
    languageOptions: { 
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        ecmaFeatures: {
          jsx: true
        }
      }
    }
  },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  {
    rules: {
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      '@typescript-eslint/no-unused-vars': 'warn',
      '@typescript-eslint/no-unused-expressions': 'off',
      'no-console': 'warn'
    },
    settings: {
      react: {
        version: 'detect'
      }
    }
  }
];

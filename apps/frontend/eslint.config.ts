export default {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      es6: true,
      browser: true,
      jsx: true,
    },
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
    'plugin:prettier/recommended',
  ],
  rules: {
    'no-restricted-imports': [
      'error',
      {
        paths: [
          {
            name: 'styled-components',
            importNames: ['useTheme'],
            message: 'Please import useTheme from hooks/useTheme instead.',
          },
        ],
        patterns: [
          {
            group: ['ts-toolbelt/out/*'],
            message: 'Please import from ts-toolbelt instead.',
          },
        ],
      },
    ],
    'no-unused-vars': 'off',
    'react/no-children-prop': 'off',
    'react/jsx-curly-brace-presence': [
      'error',
      {
        props: 'always',
        children: 'always',
        propElementValues: 'always',
      },
    ],
    '@typescript-eslint/ban-ts-comment': 'warn',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        varsIgnorePattern: '^_',
      },
    ],
    'prettier/prettier': [
      'error',
      {
        endOfLine: 'auto',
      },
    ],
  },
  ignorePatterns: ['src/generated/*.tsx', '**/node_modules/**'],
  settings: {
    react: {
      version: 'detect',
    },
  },
}

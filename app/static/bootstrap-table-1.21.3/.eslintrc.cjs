module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    'array-bracket-newline': ['error', 'consistent'],
    'array-bracket-spacing': ['error', 'never'],
    'array-element-newline': 'off',
    'arrow-parens': ['error', 'as-needed'],
    'arrow-spacing': ['error', { after: true, before: true }],
    'block-spacing': 'error',
    'brace-style': ['error', '1tbs'],
    camelcase: 'off',
    'comma-dangle': ['error', 'never'],
    'comma-spacing': ['error', { after: true, before: false }],
    'comma-style': 'off',
    'computed-property-spacing': ['error', 'never'],
    'default-case': 'error',
    'dot-location': ['error', 'property'],
    'eol-last': ['error', 'always'],
    eqeqeq: 'error',
    'func-call-spacing': ['error', 'never'],
    'guard-for-in': 'warn',
    indent: ['error', 2, {
      ArrayExpression: 1,
      CallExpression: { arguments: 1 },
      FunctionDeclaration: { parameters: 'first' },
      ImportDeclaration: 'first',
      MemberExpression: 1,
      ObjectExpression: 1,
      SwitchCase: 1
    }],
    'jsdoc/require-jsdoc': 0,
    'key-spacing': ['error', { afterColon: true, beforeColon: false, mode: 'strict' }],
    'keyword-spacing': ['error', { after: true, before: true }],
    'linebreak-style': 'off',
    'line-comment-position': 'off',
    'lines-around-comment': 'off',
    'lines-between-class-members': ['error', 'always'],
    'max-len': 'off',
    'max-statements-per-line': ['error', { max: 1 }],
    'multiline-ternary': 'off',
    'no-alert': 'error',
    'no-async-promise-executor': 'off',
    'no-case-declarations': 'off',
    'no-console': ['warn', { allow: ['warn', 'error', 'trace'] }],
    'no-duplicate-imports': 'error',
    'no-else-return': ['error', { allowElseIf: false }],
    'no-extra-parens': 'error',
    'no-lonely-if': 'error',
    'no-mixed-spaces-and-tabs': 'error',
    'no-multi-spaces': 'error',
    'no-multi-str': 'error',
    'no-multiple-empty-lines': 'error',
    'no-new-func': 'error',
    'no-param-reassign': 'off',
    'no-prototype-builtins': 'off',
    'no-return-assign': 'error',
    'no-return-await': 'error',
    'no-sequences': 'error',
    'no-tabs': 'error',
    'no-throw-literal': 'error',
    'no-trailing-spaces': 'error',
    'no-undef-init': 'error',
    'no-unused-vars': 'error',
    'no-use-before-define': 'warn',
    'no-useless-constructor': 'warn',
    'no-var': 'error',
    'no-void': 'error',
    'no-whitespace-before-property': 'error',
    'object-curly-spacing': ['error', 'always'],
    'object-shorthand': 'error',
    'one-var': ['error', 'never'],
    'operator-assignment': ['error', 'always'],
    'operator-linebreak': ['error', 'after'],
    'padding-line-between-statements': [
      'error',
      { blankLine: 'always', next: '*', prev: ['const', 'let', 'var'] },
      { blankLine: 'any', next: ['const', 'let', 'var'], prev: ['const', 'let', 'var'] },
      { blankLine: 'always', next: 'export', prev: '*' }
    ],
    'prefer-const': 'error',
    'prefer-spread': 'error',
    'prefer-template': 'error',
    'quote-props': ['error', 'as-needed'],
    quotes: ['error', 'single'],
    semi: ['error', 'never'],
    'semi-spacing': ['error', { after: true, before: false }],
    'semi-style': ['error', 'last'],
    'sort-imports': 'off',
    'space-before-blocks': ['error', { classes: 'always', functions: 'always', keywords: 'always' }],
    'space-before-function-paren': ['error', 'always'],
    'space-in-parens': ['error', 'never'],
    'space-infix-ops': 'error',
    'spaced-comment': ['error', 'always'],
    'switch-colon-spacing': 'error',
    'template-curly-spacing': ['error', 'never']
  },
  globals: {
    $: true,
    jQuery: true
  }
}

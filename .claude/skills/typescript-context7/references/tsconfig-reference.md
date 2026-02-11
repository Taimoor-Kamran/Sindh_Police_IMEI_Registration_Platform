# TSConfig Reference

## Compiler Options

### Type Checking

```json
{
  "compilerOptions": {
    "strict": true,                    // Enable all strict options
    "noImplicitAny": true,             // Error on implied 'any' type
    "strictNullChecks": true,          // Enable strict null checks
    "strictFunctionTypes": true,       // Strict function type checking
    "strictBindCallApply": true,       // Strict bind/call/apply
    "strictPropertyInitialization": true, // Strict property initialization
    "noImplicitThis": true,            // Error on 'this' with implied 'any'
    "useUnknownInCatchVariables": true, // Default catch to 'unknown'
    "alwaysStrict": true,              // Parse in strict mode
    "noUnusedLocals": true,            // Error on unused locals
    "noUnusedParameters": true,        // Error on unused parameters
    "exactOptionalPropertyTypes": true, // Differentiate undefined vs missing
    "noImplicitReturns": true,         // Error on missing returns
    "noFallthroughCasesInSwitch": true, // Error on fallthrough cases
    "noUncheckedIndexedAccess": true,  // Add undefined to index signatures
    "noImplicitOverride": true,        // Require 'override' modifier
    "noPropertyAccessFromIndexSignature": true // Require bracket notation
  }
}
```

### Modules

```json
{
  "compilerOptions": {
    "module": "ESNext",                // Module code generation
    "moduleResolution": "bundler",     // Module resolution strategy
    "resolveJsonModule": true,         // Allow importing JSON
    "esModuleInterop": true,           // Emit helpers for interop
    "allowSyntheticDefaultImports": true, // Allow default imports
    "isolatedModules": true,           // Ensure safe transpilation
    "verbatimModuleSyntax": true,      // Preserve import/export syntax
    "moduleDetection": "force"         // Treat all files as modules
  }
}
```

### Emit

```json
{
  "compilerOptions": {
    "target": "ES2022",                // ECMAScript target version
    "lib": ["ES2022", "DOM"],          // Library files to include
    "outDir": "./dist",                // Output directory
    "rootDir": "./src",                // Root directory of source
    "declaration": true,               // Generate .d.ts files
    "declarationMap": true,            // Generate declaration maps
    "sourceMap": true,                 // Generate source maps
    "inlineSources": true,             // Include sources in maps
    "removeComments": false,           // Keep comments
    "noEmit": true,                    // Don't emit outputs
    "noEmitOnError": true,             // Don't emit on errors
    "importHelpers": true,             // Import helpers from tslib
    "downlevelIteration": true         // Full iteration support
  }
}
```

### JavaScript Support

```json
{
  "compilerOptions": {
    "allowJs": true,                   // Allow JavaScript files
    "checkJs": true,                   // Check JavaScript files
    "maxNodeModuleJsDepth": 1          // Max depth for node_modules
  }
}
```

### Interop Constraints

```json
{
  "compilerOptions": {
    "forceConsistentCasingInFileNames": true, // Consistent file casing
    "allowArbitraryExtensions": true,  // Allow arbitrary extensions
    "customConditions": ["development"] // Custom package.json conditions
  }
}
```

### Path Mapping

```json
{
  "compilerOptions": {
    "baseUrl": ".",                    // Base directory for paths
    "paths": {                         // Path aliases
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    },
    "rootDirs": ["src", "generated"]   // Virtual directory roots
  }
}
```

## Common Configurations

### React/Next.js
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "incremental": true,
    "plugins": [{ "name": "next" }]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Node.js
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Library
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "composite": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### Monorepo (Project References)
```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true,
    "incremental": true
  },
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/ui" },
    { "path": "./packages/utils" }
  ]
}
```

## Include/Exclude

```json
{
  "include": [
    "src/**/*",
    "types/**/*.d.ts"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "**/*.spec.ts",
    "**/*.test.ts"
  ],
  "files": [
    "src/index.ts"
  ]
}
```

## Extends

```json
{
  "extends": "@tsconfig/node20/tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist"
  }
}
```

## Common Base Configs

| Package | Use Case |
|---------|----------|
| `@tsconfig/node20` | Node.js 20+ |
| `@tsconfig/node18` | Node.js 18+ |
| `@tsconfig/strictest` | Maximum strictness |
| `@tsconfig/recommended` | Recommended defaults |

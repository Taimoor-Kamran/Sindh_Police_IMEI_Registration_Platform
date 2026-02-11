# Envconfig Common Patterns

Quick reference for kelseyhightower/envconfig Go library patterns.

## Basic Usage

### Simple Configuration

```go
package main

import (
    "log"
    "github.com/kelseyhightower/envconfig"
)

type Config struct {
    Debug    bool
    Port     int
    Host     string
    Database string
}

func main() {
    var cfg Config
    err := envconfig.Process("myapp", &cfg)
    if err != nil {
        log.Fatal(err)
    }
    // Environment variables: MYAPP_DEBUG, MYAPP_PORT, MYAPP_HOST, MYAPP_DATABASE
}
```

### MustProcess (Panic on Error)

```go
func main() {
    var cfg Config
    envconfig.MustProcess("myapp", &cfg)
    // Panics if environment variables are missing/invalid
}
```

## Struct Tags

### Available Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `envconfig` | Custom env var name | `envconfig:"db_host"` |
| `default` | Default value | `default:"localhost"` |
| `required` | Must be set | `required:"true"` |
| `split_words` | CamelCase to SNAKE_CASE | `split_words:"true"` |
| `ignored` | Skip field | `ignored:"true"` |
| `desc` | Description for usage | `desc:"Database host"` |

### Example with All Tags

```go
type Config struct {
    // MYAPP_HOST (default: localhost)
    Host string `default:"localhost" desc:"Server hostname"`

    // MYAPP_PORT (required, no default)
    Port int `required:"true" desc:"Server port"`

    // MYAPP_DATABASE_URL (custom name)
    DatabaseURL string `envconfig:"DATABASE_URL" required:"true"`

    // MYAPP_MAX_CONNECTIONS (split_words converts MaxConnections)
    MaxConnections int `split_words:"true" default:"10"`

    // Ignored field - not read from environment
    InternalCache bool `ignored:"true"`
}
```

## Default Values

### Simple Defaults

```go
type Config struct {
    Port    int    `default:"8080"`
    Host    string `default:"0.0.0.0"`
    Debug   bool   `default:"false"`
    Timeout int    `default:"30"`
}
```

### Complex Type Defaults

```go
type Config struct {
    // Duration: parsed as time.Duration
    Timeout time.Duration `default:"30s"`

    // Slice: comma-separated
    Hosts []string `default:"localhost,127.0.0.1"`

    // URL: parsed as url.URL
    BaseURL url.URL `default:"http://localhost:8080"`
}
```

## Required Fields

```go
type Config struct {
    // Will error if MYAPP_API_KEY is not set
    APIKey string `required:"true"`

    // Will error if MYAPP_DATABASE_URL is not set
    DatabaseURL string `envconfig:"DATABASE_URL" required:"true"`

    // Optional - no error if missing
    Debug bool
}
```

## Custom Environment Variable Names

```go
type Config struct {
    // Uses DB_HOST instead of MYAPP_DB_HOST
    DBHost string `envconfig:"DB_HOST"`

    // Uses DATABASE_URL instead of MYAPP_DATABASE_URL
    DatabaseURL string `envconfig:"DATABASE_URL"`

    // Uses full path without prefix
    AWSRegion string `envconfig:"AWS_REGION"`
}
```

## Split Words (CamelCase to SNAKE_CASE)

```go
type Config struct {
    // MYAPP_MAX_IDLE_CONNECTIONS
    MaxIdleConnections int `split_words:"true"`

    // MYAPP_READ_TIMEOUT
    ReadTimeout time.Duration `split_words:"true" default:"30s"`

    // MYAPP_SSL_ENABLED
    SSLEnabled bool `split_words:"true" default:"true"`
}
```

## Custom Decoders

### Decoder Interface

```go
// Implement envconfig.Decoder for custom parsing
type Decoder interface {
    Decode(value string) error
}
```

### Custom Type Example

```go
type LogLevel int

const (
    LogDebug LogLevel = iota
    LogInfo
    LogWarn
    LogError
)

func (l *LogLevel) Decode(value string) error {
    switch strings.ToLower(value) {
    case "debug":
        *l = LogDebug
    case "info":
        *l = LogInfo
    case "warn":
        *l = LogWarn
    case "error":
        *l = LogError
    default:
        return fmt.Errorf("unknown log level: %s", value)
    }
    return nil
}

type Config struct {
    LogLevel LogLevel `default:"info"`
}
```

### Setter Interface

```go
// Alternative to Decoder - receives full value
type Setter interface {
    Set(value string) error
}
```

## Usage Generation

### Print Usage to Stderr

```go
func main() {
    var cfg Config
    err := envconfig.Process("myapp", &cfg)
    if err != nil {
        envconfig.Usage("myapp", &cfg)
        log.Fatal(err)
    }
}
```

### Custom Usage Format

```go
func main() {
    var cfg Config

    // Usage with custom writer and format
    envconfig.Usagef("myapp", &cfg, os.Stdout, envconfig.DefaultTableFormat)

    // Available formats:
    // - envconfig.DefaultTableFormat
    // - envconfig.DefaultListFormat
}
```

### Usage Output Example

```
KEY                    TYPE        DEFAULT     REQUIRED    DESCRIPTION
MYAPP_HOST             String      localhost               Server hostname
MYAPP_PORT             Integer                 true        Server port
MYAPP_DATABASE_URL     String                  true        Database connection URL
MYAPP_MAX_CONNECTIONS  Integer     10                      Maximum DB connections
```

## Nested Structs

```go
type DatabaseConfig struct {
    Host     string `default:"localhost"`
    Port     int    `default:"5432"`
    Name     string `required:"true"`
    User     string `required:"true"`
    Password string `required:"true"`
}

type Config struct {
    Debug    bool
    Database DatabaseConfig
}

// Environment variables:
// MYAPP_DEBUG
// MYAPP_DATABASE_HOST
// MYAPP_DATABASE_PORT
// MYAPP_DATABASE_NAME
// MYAPP_DATABASE_USER
// MYAPP_DATABASE_PASSWORD
```

## Validation with CheckDisallowed

```go
func main() {
    var cfg Config

    // Process config
    err := envconfig.Process("myapp", &cfg)
    if err != nil {
        log.Fatal(err)
    }

    // Check for unknown MYAPP_* variables
    err = envconfig.CheckDisallowed("myapp", &cfg)
    if err != nil {
        log.Printf("Warning: %v", err)
    }
}
```

## Common Patterns

### Database Configuration

```go
type DatabaseConfig struct {
    Driver   string        `default:"postgres"`
    Host     string        `default:"localhost"`
    Port     int           `default:"5432"`
    Name     string        `required:"true"`
    User     string        `required:"true"`
    Password string        `required:"true"`
    SSLMode  string        `split_words:"true" default:"disable"`
    MaxConns int           `split_words:"true" default:"10"`
    Timeout  time.Duration `default:"30s"`
}

func (d *DatabaseConfig) DSN() string {
    return fmt.Sprintf("%s://%s:%s@%s:%d/%s?sslmode=%s",
        d.Driver, d.User, d.Password, d.Host, d.Port, d.Name, d.SSLMode)
}
```

### Server Configuration

```go
type ServerConfig struct {
    Host         string        `default:"0.0.0.0"`
    Port         int           `default:"8080"`
    ReadTimeout  time.Duration `split_words:"true" default:"15s"`
    WriteTimeout time.Duration `split_words:"true" default:"15s"`
    IdleTimeout  time.Duration `split_words:"true" default:"60s"`
}
```

### Feature Flags

```go
type FeatureFlags struct {
    EnableNewUI     bool `split_words:"true" default:"false"`
    EnableAnalytics bool `split_words:"true" default:"true"`
    BetaFeatures    bool `split_words:"true" default:"false"`
}
```

## Tips

1. **Use prefixes**: Always use a prefix like `envconfig.Process("myapp", &cfg)` to namespace your variables
2. **Document with desc**: Use `desc` tag for self-documenting configuration
3. **Validate early**: Call `envconfig.Process` at startup to fail fast on missing config
4. **Use split_words**: Makes environment variables more readable (`MAX_CONNECTIONS` vs `MAXCONNECTIONS`)
5. **Combine tags**: Tags can be combined: `required:"true" default:"value"` (default ignored if required)

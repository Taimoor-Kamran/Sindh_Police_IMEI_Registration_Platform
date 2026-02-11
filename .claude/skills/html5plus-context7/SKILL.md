---
name: html5plus-context7
description: Token-efficient HTML5+ (DCloud) documentation fetcher using Context7 MCP. Fetches code examples, API references, and best practices for HTML5+ native mobile APIs including camera, file system, geolocation, push notifications, and device features. Use when users ask about HTML5+ APIs, uni-app native plugins, HBuilder development, 5+App runtime, or DCloud mobile development. Triggers include questions like "How do I use plus.camera", "HTML5+ file system API", "uni-app native features", or any request for DCloud/HTML5+ documentation.
---

# HTML5+ Context7 Documentation Fetcher

Fetch HTML5+ (DCloud) library documentation with automatic token reduction via shell pipeline.

## What is HTML5+?

**HTML5+** (HTML5 Plus) is a JavaScript runtime specification by DCloud that extends HTML5 with native mobile capabilities:

- **Runtime**: Native JavaScript bridge for iOS/Android
- **IDE**: HBuilder/HBuilderX development environment
- **Frameworks**: uni-app, 5+App, MUI
- **Target**: Hybrid mobile apps, mini-programs, H5 apps

### Core API Modules

| Module | Description | Key APIs |
|--------|-------------|----------|
| `plus.camera` | Camera access | `captureImage()`, `startVideoCapture()` |
| `plus.io` | File system | `FileReader`, `FileWriter`, `requestFileSystem()` |
| `plus.geolocation` | GPS/Location | `getCurrentPosition()`, `watchPosition()` |
| `plus.push` | Push notifications | `createMessage()`, `addEventListener()` |
| `plus.barcode` | QR/Barcode scanner | `Barcode.scan()`, `create()` |
| `plus.nativeUI` | Native UI elements | `toast()`, `alert()`, `actionSheet()` |
| `plus.sqlite` | SQLite database | `openDatabase()`, `executeSql()` |
| `plus.bluetooth` | Bluetooth LE | `startScan()`, `connect()` |
| `plus.payment` | Payment integration | `request()` (WeChat Pay, Alipay) |
| `plus.device` | Device info | `uuid`, `model`, `vendor` |

## Quick Start

**Always use the token-efficient shell pipeline:**

```bash
# Automatic library resolution + filtering
bash scripts/fetch-docs.sh --library html5plus --topic <topic>

# Examples:
bash scripts/fetch-docs.sh --library html5plus --topic camera
bash scripts/fetch-docs.sh --library html5plus --topic file-system
bash scripts/fetch-docs.sh --library html5plus --topic geolocation
bash scripts/fetch-docs.sh --library html5plus --topic push-notification
```

**Alternative library names to try:**
```bash
bash scripts/fetch-docs.sh --library dcloud --topic <topic>
bash scripts/fetch-docs.sh --library "uni-app" --topic native
bash scripts/fetch-docs.sh --library hbuilder --topic <topic>
```

## Standard Workflow

### 1. Identify the HTML5+ Module

Extract from user query:
- **Module**: camera, io, geolocation, push, barcode, nativeUI, etc.
- **Operation**: capture, read, write, scan, etc.

### 2. Fetch with Shell Pipeline

```bash
bash scripts/fetch-docs.sh --library html5plus --topic <module> --verbose
```

The `--verbose` flag shows token savings statistics.

### 3. Use Filtered Output

The script automatically:
- Fetches full documentation (stays in subprocess)
- Filters to code examples + API signatures + key notes
- Returns only essential content to Claude

## Parameters

### Basic Usage

```bash
bash scripts/fetch-docs.sh [OPTIONS]
```

**Required (pick one):**
- `--library <name>` - Library name (e.g., "html5plus", "dcloud", "uni-app")
- `--library-id <id>` - Direct Context7 ID (faster, skips resolution)

**Optional:**
- `--topic <topic>` - Specific module/feature to focus on
- `--mode <code|info>` - code for examples (default), info for concepts
- `--page <1-10>` - Pagination for more results
- `--verbose` - Show token savings statistics

## Workflow Patterns

### Pattern 1: Camera API

User asks: "How do I capture a photo with HTML5+?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic camera --verbose
```

**Expected APIs:**
```javascript
// Capture image
plus.camera.getCamera().captureImage(
  function(path) { console.log('Photo saved:', path); },
  function(error) { console.error(error); },
  { filename: 'photo.jpg', quality: 80 }
);
```

### Pattern 2: File System Operations

User asks: "How do I read and write files in HTML5+?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic "file system" --mode code
```

**Expected APIs:**
```javascript
// Request file system
plus.io.requestFileSystem(
  plus.io.PRIVATE_WWW,
  function(fs) {
    // Read file
    fs.root.getFile('data.txt', {create: false}, function(fileEntry) {
      fileEntry.file(function(file) {
        var reader = new plus.io.FileReader();
        reader.onloadend = function(e) {
          console.log(this.result);
        };
        reader.readAsText(file);
      });
    });
  }
);
```

### Pattern 3: Geolocation

User asks: "How do I get GPS location?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic geolocation
```

**Expected APIs:**
```javascript
plus.geolocation.getCurrentPosition(
  function(position) {
    console.log('Latitude:', position.coords.latitude);
    console.log('Longitude:', position.coords.longitude);
  },
  function(error) {
    console.error('Error:', error.message);
  },
  { enableHighAccuracy: true }
);
```

### Pattern 4: Push Notifications

User asks: "How do I handle push notifications?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic push --mode code
```

**Expected APIs:**
```javascript
// Create local notification
plus.push.createMessage('Notification content', 'payload', {
  title: 'Notification Title',
  sound: 'default',
  cover: false
});

// Listen for push events
plus.push.addEventListener('receive', function(msg) {
  console.log('Received:', msg.payload);
});
```

### Pattern 5: Barcode Scanner

User asks: "How do I scan QR codes?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic barcode
```

**Expected APIs:**
```javascript
plus.barcode.scan(
  'barcodeContainer',
  function(type, result) {
    console.log('Scanned:', result);
  },
  function(error) {
    console.error(error);
  },
  { frameColor: '#1D8CE0', scanbarColor: '#1D8CE0' }
);
```

### Pattern 6: Native UI

User asks: "How do I show alerts and toasts?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic nativeUI
```

**Expected APIs:**
```javascript
// Toast
plus.nativeUI.toast('Message displayed!');

// Alert
plus.nativeUI.alert('Alert message', function() {
  console.log('Alert closed');
}, 'Title', 'OK');

// Action Sheet
plus.nativeUI.actionSheet({
  title: 'Choose an option',
  cancel: 'Cancel',
  buttons: [
    { title: 'Option 1' },
    { title: 'Option 2' }
  ]
}, function(e) {
  console.log('Selected index:', e.index);
});
```

### Pattern 7: SQLite Database

User asks: "How do I use SQLite in HTML5+?"

```bash
bash scripts/fetch-docs.sh --library html5plus --topic sqlite
```

**Expected APIs:**
```javascript
// Open database
plus.sqlite.openDatabase({
  name: 'mydb',
  path: '_doc/mydb.db',
  success: function(db) {
    // Execute SQL
    plus.sqlite.executeSql({
      name: 'mydb',
      sql: 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)',
      success: function() {
        console.log('Table created');
      }
    });
  }
});
```

## Best Practices

### 1. Permission Handling

Always check and request permissions before using device features:

```javascript
// Check permission
plus.android.requestPermissions(
  ['android.permission.CAMERA'],
  function(e) {
    if (e.granted.length > 0) {
      // Permission granted, proceed
      capturePhoto();
    } else {
      // Permission denied
      plus.nativeUI.toast('Camera permission required');
    }
  }
);
```

### 2. Platform Detection

Check platform before using platform-specific features:

```javascript
if (plus.os.name === 'Android') {
  // Android-specific code
} else if (plus.os.name === 'iOS') {
  // iOS-specific code
}
```

### 3. Event Handling

Use proper event listeners for app lifecycle:

```javascript
document.addEventListener('plusready', function() {
  // HTML5+ APIs are ready
});

document.addEventListener('pause', function() {
  // App going to background
});

document.addEventListener('resume', function() {
  // App returning to foreground
});
```

### 4. Error Handling

Always handle errors gracefully:

```javascript
try {
  plus.camera.getCamera().captureImage(successCb, errorCb, options);
} catch (e) {
  console.error('Camera error:', e.message);
  plus.nativeUI.toast('Camera not available');
}
```

## Token Efficiency

**How it works:**

1. `fetch-docs.sh` calls `fetch-raw.sh` (which uses `mcp-client.py`)
2. Full response stays in subprocess memory
3. Shell filters (awk/grep/sed) extract essentials (0 LLM tokens used)
4. Returns filtered output to Claude

**Do NOT use `mcp-client.py` directly** - it bypasses filtering and wastes tokens.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Library not found | Try "dcloud", "uni-app", or "hbuilder" as library name |
| No results for topic | Use broader terms like "device", "storage", "ui" |
| Need more examples | Increase page: `--page 2` |
| Want full context | Use `--mode info` for explanations |

## References

- [HTML5+ Specification](http://www.html5plus.org/doc/h5p.html)
- [DCloud Documentation](https://dcloud.io/docs)
- [uni-app Documentation](https://uniapp.dcloud.io/)
- [references/html5plus-api.md](references/html5plus-api.md) - Quick API reference

## Implementation Notes

**Components (for reference only, use fetch-docs.sh):**
- `mcp-client.py` - Universal MCP client (foundation)
- `fetch-raw.sh` - MCP wrapper
- `extract-code-blocks.sh` - Code example filter (awk)
- `extract-signatures.sh` - API signature filter (awk)
- `extract-notes.sh` - Important notes filter (grep)
- `fetch-docs.sh` - **Main orchestrator (ALWAYS USE THIS)**

**Architecture:**
Shell pipeline processes documentation in subprocess, keeping full response out of Claude's context. Only filtered essentials enter the LLM context, achieving significant token savings with 100% functionality preserved.

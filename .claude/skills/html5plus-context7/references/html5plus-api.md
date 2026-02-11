# HTML5+ API Quick Reference

*Complete API reference for DCloud HTML5+ runtime*

## Core Modules

### plus.camera

Camera capture and video recording.

```javascript
// Get camera instance
var camera = plus.camera.getCamera();

// Capture image
camera.captureImage(
  function(path) { /* success */ },
  function(error) { /* error */ },
  {
    filename: 'photo.jpg',  // Output filename
    quality: 80,            // JPEG quality (1-100)
    resolution: 'high',     // 'high', 'medium', 'low'
    format: 'jpg'           // 'jpg' or 'png'
  }
);

// Capture video
camera.startVideoCapture(
  function(path) { /* success */ },
  function(error) { /* error */ },
  {
    filename: 'video.mp4',
    resolution: 'high',
    optimize: true
  }
);
camera.stopVideoCapture();
```

### plus.io

File system operations.

```javascript
// Request file system
plus.io.requestFileSystem(
  plus.io.PRIVATE_DOC,  // PRIVATE_WWW, PRIVATE_DOC, PUBLIC_DOCUMENTS, PUBLIC_DOWNLOADS
  function(fs) {
    // Get root directory
    var root = fs.root;

    // Get file
    root.getFile('data.txt', { create: true }, function(fileEntry) {
      // Read
      fileEntry.file(function(file) {
        var reader = new plus.io.FileReader();
        reader.onloadend = function(e) { console.log(this.result); };
        reader.readAsText(file);
      });

      // Write
      fileEntry.createWriter(function(writer) {
        writer.write('content');
      });
    });

    // Get directory
    root.getDirectory('subdir', { create: true }, function(dirEntry) {
      // List contents
      var reader = dirEntry.createReader();
      reader.readEntries(function(entries) {
        entries.forEach(function(entry) {
          console.log(entry.name, entry.isFile);
        });
      });
    });
  }
);

// File path constants
plus.io.PRIVATE_WWW      // App private www directory
plus.io.PRIVATE_DOC      // App private documents
plus.io.PUBLIC_DOCUMENTS // Public documents folder
plus.io.PUBLIC_DOWNLOADS // Public downloads folder
```

### plus.geolocation

GPS and location services.

```javascript
// Get current position
plus.geolocation.getCurrentPosition(
  function(position) {
    var coords = position.coords;
    console.log('Latitude:', coords.latitude);
    console.log('Longitude:', coords.longitude);
    console.log('Altitude:', coords.altitude);
    console.log('Accuracy:', coords.accuracy);
    console.log('Speed:', coords.speed);
    console.log('Heading:', coords.heading);
  },
  function(error) {
    console.log('Error code:', error.code);
    console.log('Error message:', error.message);
  },
  {
    enableHighAccuracy: true,  // Use GPS (slower but accurate)
    timeout: 10000,            // Timeout in ms
    maximumAge: 0,             // Max cached age in ms
    provider: 'system',        // 'system', 'baidu', 'amap'
    coordsType: 'wgs84'        // 'wgs84', 'gcj02', 'bd09'
  }
);

// Watch position changes
var watchId = plus.geolocation.watchPosition(
  function(position) { /* success */ },
  function(error) { /* error */ },
  { enableHighAccuracy: true }
);

// Stop watching
plus.geolocation.clearWatch(watchId);
```

### plus.push

Push notifications.

```javascript
// Create local notification
plus.push.createMessage(
  'Notification body text',  // Content
  'custom_payload',          // Payload (received in event)
  {
    title: 'Notification Title',
    sound: 'default',        // 'none', 'default', or file path
    cover: false,            // Replace existing notification
    when: new Date(),        // Schedule time
    delay: 0                 // Delay in ms
  }
);

// Get all notifications
var messages = plus.push.getAllMessage();

// Clear all notifications
plus.push.clear();

// Event listeners
plus.push.addEventListener('click', function(msg) {
  // User clicked notification
  console.log('Payload:', msg.payload);
});

plus.push.addEventListener('receive', function(msg) {
  // Notification received
  console.log('Title:', msg.title);
  console.log('Content:', msg.content);
});

// Get client info (for remote push)
var info = plus.push.getClientInfo();
console.log('Client ID:', info.clientid);
console.log('Token:', info.token);
```

### plus.barcode

QR code and barcode scanner.

```javascript
// Scan barcode (fullscreen)
plus.barcode.scan(
  'containerElementId',      // Container element ID
  function(type, result) {
    console.log('Type:', type);    // Barcode type
    console.log('Result:', result); // Scanned content
  },
  function(error) {
    console.log('Error:', error.message);
  },
  {
    frameColor: '#1D8CE0',   // Scanner frame color
    scanbarColor: '#1D8CE0', // Scanner line color
    background: '#000000',   // Background color
    filters: [               // Barcode types to scan
      plus.barcode.QR,
      plus.barcode.EAN13,
      plus.barcode.CODE128
    ]
  }
);

// Create barcode control
var barcode = plus.barcode.create(
  'containerElementId',
  [plus.barcode.QR],
  { frameColor: '#1D8CE0' }
);
barcode.start();
barcode.cancel();
barcode.close();

// Barcode types
plus.barcode.QR        // QR Code
plus.barcode.EAN13     // EAN-13
plus.barcode.EAN8      // EAN-8
plus.barcode.UPCA      // UPC-A
plus.barcode.UPCE      // UPC-E
plus.barcode.CODE128   // Code 128
plus.barcode.CODE39    // Code 39
plus.barcode.CODABAR   // Codabar
plus.barcode.ITF       // ITF
plus.barcode.PDF417    // PDF417
plus.barcode.DATAMATRIX // Data Matrix
```

### plus.nativeUI

Native UI components.

```javascript
// Toast
plus.nativeUI.toast('Message', { duration: 'short' }); // 'short' or 'long'

// Alert
plus.nativeUI.alert(
  'Alert message',
  function() { /* closed */ },
  'Title',
  'OK'
);

// Confirm
plus.nativeUI.confirm(
  'Confirm message',
  function(e) {
    if (e.index === 0) { /* confirmed */ }
  },
  'Title',
  ['OK', 'Cancel']
);

// Prompt
plus.nativeUI.prompt(
  'Enter value:',
  function(e) {
    if (e.index === 0) {
      console.log('Input:', e.value);
    }
  },
  'Title',
  'Placeholder',
  ['OK', 'Cancel']
);

// Action Sheet
plus.nativeUI.actionSheet(
  {
    title: 'Choose option',
    cancel: 'Cancel',
    buttons: [
      { title: 'Option 1', color: '#FF0000' },
      { title: 'Option 2' }
    ]
  },
  function(e) {
    console.log('Selected:', e.index); // 0 = cancel, 1+ = buttons
  }
);

// Loading indicator
var loading = plus.nativeUI.showWaiting('Loading...');
// ... later
loading.close();

// Progress dialog
var progress = plus.nativeUI.showProgress('Loading');
progress.setProgress(50); // 0-100
progress.close();

// Picker (date/time)
plus.nativeUI.pickDate(
  function(e) {
    console.log('Date:', e.date);
  },
  function(e) { /* cancelled */ },
  {
    title: 'Select Date',
    date: new Date(),
    minDate: new Date(2020, 0, 1),
    maxDate: new Date(2030, 11, 31)
  }
);

plus.nativeUI.pickTime(
  function(e) {
    console.log('Hours:', e.date.getHours());
    console.log('Minutes:', e.date.getMinutes());
  },
  function(e) { /* cancelled */ }
);
```

### plus.sqlite

SQLite database.

```javascript
// Open database
plus.sqlite.openDatabase({
  name: 'mydb',
  path: '_doc/mydb.db',
  success: function(db) { /* opened */ },
  fail: function(e) { console.log(e.message); }
});

// Check if database is open
var isOpen = plus.sqlite.isOpenDatabase({ name: 'mydb', path: '_doc/mydb.db' });

// Execute SQL
plus.sqlite.executeSql({
  name: 'mydb',
  sql: 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)',
  success: function() { /* success */ },
  fail: function(e) { console.log(e.message); }
});

// Insert data
plus.sqlite.executeSql({
  name: 'mydb',
  sql: "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')"
});

// Query data
plus.sqlite.selectSql({
  name: 'mydb',
  sql: 'SELECT * FROM users WHERE id = ?',
  args: [1],
  success: function(data) {
    data.forEach(function(row) {
      console.log(row.name, row.email);
    });
  }
});

// Close database
plus.sqlite.closeDatabase({
  name: 'mydb',
  success: function() { /* closed */ }
});

// Transaction
plus.sqlite.transaction({
  name: 'mydb',
  operation: 'begin',  // 'begin', 'commit', 'rollback'
  success: function() { /* success */ }
});
```

### plus.device

Device information.

```javascript
// Device identifiers
plus.device.uuid        // Unique device ID
plus.device.imei        // IMEI (Android only, requires permission)
plus.device.imsi        // IMSI (Android only)
plus.device.model       // Device model
plus.device.vendor      // Device manufacturer

// Screen info
plus.screen.width       // Screen width (logical pixels)
plus.screen.height      // Screen height (logical pixels)
plus.screen.scale       // Screen scale factor
plus.screen.dpiX        // Horizontal DPI
plus.screen.dpiY        // Vertical DPI

// Display info
plus.display.resolutionWidth   // Physical width
plus.display.resolutionHeight  // Physical height

// Network type
plus.networkinfo.getCurrentType(); // 'ethernet', 'wifi', 'cell2g', 'cell3g', 'cell4g', 'none', 'unknown'

// OS info
plus.os.name      // 'Android' or 'iOS'
plus.os.version   // OS version string
plus.os.language  // Device language
plus.os.vendor    // 'Google' or 'Apple'

// Set screen brightness
plus.screen.setBrightness(0.8); // 0.0 - 1.0
var brightness = plus.screen.getBrightness();

// Keep screen on
plus.device.setWakelock(true);
```

### plus.bluetooth

Bluetooth Low Energy (BLE).

```javascript
// Open Bluetooth adapter
plus.bluetooth.openBluetoothAdapter({
  success: function() { /* opened */ },
  fail: function(e) { console.log(e.errMsg); }
});

// Start scanning
plus.bluetooth.startBluetoothDevicesDiscovery({
  services: ['FFF0'],  // Filter by service UUIDs
  allowDuplicatesKey: false,
  success: function() { /* scanning */ }
});

// Listen for device found
plus.bluetooth.onBluetoothDeviceFound(function(devices) {
  devices.forEach(function(device) {
    console.log('Name:', device.name);
    console.log('ID:', device.deviceId);
    console.log('RSSI:', device.RSSI);
  });
});

// Stop scanning
plus.bluetooth.stopBluetoothDevicesDiscovery();

// Connect to device
plus.bluetooth.createBLEConnection({
  deviceId: 'device_id_here',
  success: function() { /* connected */ }
});

// Get services
plus.bluetooth.getBLEDeviceServices({
  deviceId: 'device_id_here',
  success: function(res) {
    res.services.forEach(function(service) {
      console.log('Service UUID:', service.uuid);
    });
  }
});

// Get characteristics
plus.bluetooth.getBLEDeviceCharacteristics({
  deviceId: 'device_id_here',
  serviceId: 'service_uuid',
  success: function(res) {
    res.characteristics.forEach(function(char) {
      console.log('Char UUID:', char.uuid);
      console.log('Properties:', char.properties);
    });
  }
});

// Read characteristic
plus.bluetooth.readBLECharacteristicValue({
  deviceId: 'device_id',
  serviceId: 'service_uuid',
  characteristicId: 'char_uuid'
});

// Write characteristic
plus.bluetooth.writeBLECharacteristicValue({
  deviceId: 'device_id',
  serviceId: 'service_uuid',
  characteristicId: 'char_uuid',
  value: new ArrayBuffer(8)  // Data to write
});

// Listen for value changes
plus.bluetooth.onBLECharacteristicValueChange(function(res) {
  console.log('Device:', res.deviceId);
  console.log('Value:', res.value);  // ArrayBuffer
});

// Disconnect
plus.bluetooth.closeBLEConnection({
  deviceId: 'device_id_here'
});

// Close adapter
plus.bluetooth.closeBluetoothAdapter();
```

### plus.payment

Payment integration.

```javascript
// Get payment channels
var channels = plus.payment.getChannels();
channels.forEach(function(channel) {
  console.log('ID:', channel.id);         // 'alipay', 'wxpay', etc.
  console.log('Description:', channel.description);
  console.log('Installed:', channel.serviceReady);
});

// Make payment request
plus.payment.request(
  channel,        // Payment channel object
  orderInfo,      // Order info string (from server)
  function(result) {
    // Payment successful
    console.log('Result:', result.rawdata);
  },
  function(error) {
    // Payment failed
    console.log('Error code:', error.code);
    switch (error.code) {
      case 62000: /* User cancelled */ break;
      case 62001: /* Payment failed */ break;
      case 62002: /* Network error */ break;
    }
  }
);
```

### plus.nfc

NFC operations (Android only).

```javascript
// Check NFC support
if (plus.nfc) {
  // Start NFC adapter
  plus.nfc.start();

  // Listen for NFC tags
  plus.nfc.onTagDiscovered(function(tag) {
    console.log('Tag ID:', tag.id);
    console.log('Tech list:', tag.techList);

    // Read NDEF message
    plus.nfc.readNdefMessage(function(message) {
      message.records.forEach(function(record) {
        console.log('Type:', record.type);
        console.log('Payload:', record.payload);
      });
    });
  });

  // Write NDEF message
  plus.nfc.writeNdefMessage({
    records: [{
      type: 'text/plain',
      payload: 'Hello NFC'
    }]
  });

  // Stop NFC adapter
  plus.nfc.stop();
}
```

## Permissions (Android)

```javascript
// Request runtime permissions
plus.android.requestPermissions(
  [
    'android.permission.CAMERA',
    'android.permission.WRITE_EXTERNAL_STORAGE',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.RECORD_AUDIO'
  ],
  function(e) {
    console.log('Granted:', e.granted);
    console.log('Denied:', e.denied);
    console.log('Denied always:', e.deniedAlways);
  }
);
```

## App Lifecycle Events

```javascript
// HTML5+ ready
document.addEventListener('plusready', function() {
  // All plus.* APIs are available
});

// App pause (background)
document.addEventListener('pause', function() {
  // Save state, stop background tasks
});

// App resume (foreground)
document.addEventListener('resume', function() {
  // Restore state, refresh data
});

// Back button (Android)
document.addEventListener('backbutton', function() {
  // Handle back button
  // Return false to prevent default
});

// Network status change
document.addEventListener('netchange', function() {
  var type = plus.networkinfo.getCurrentType();
  console.log('Network changed to:', type);
});

// New intent (deep link)
document.addEventListener('newintent', function() {
  var args = plus.runtime.arguments;
  console.log('Intent args:', args);
});
```

## Common Library IDs for Context7

When using the Context7 MCP, try these library identifiers:

| Search Term | Possible IDs |
|-------------|--------------|
| html5plus | /dcloud/html5plus |
| dcloud | /dcloud/docs |
| uni-app | /dcloudio/uni-app |
| hbuilder | /dcloud/hbuilder |
| mui | /muitech/mui |

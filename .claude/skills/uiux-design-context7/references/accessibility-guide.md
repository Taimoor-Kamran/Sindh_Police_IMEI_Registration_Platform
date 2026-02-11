# Accessibility (A11y) Guide

## WCAG 2.1 Quick Reference

### Perceivable

Users must be able to perceive the content.

#### 1.1 Text Alternatives

```html
<!-- Images with meaning -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">

<!-- Decorative images -->
<img src="decoration.png" alt="" role="presentation">

<!-- Complex images -->
<figure>
  <img src="flowchart.png" alt="User registration process flowchart">
  <figcaption>
    The registration process: 1) Enter email, 2) Verify email,
    3) Set password, 4) Complete profile
  </figcaption>
</figure>

<!-- Icons with text -->
<button>
  <svg aria-hidden="true">...</svg>
  <span>Delete</span>
</button>

<!-- Icon-only buttons -->
<button aria-label="Delete item">
  <svg aria-hidden="true">...</svg>
</button>
```

#### 1.3 Adaptable Content

```html
<!-- Semantic structure -->
<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time datetime="2024-01-15">January 15, 2024</time>
    </header>
    <section>
      <h2>Section Heading</h2>
      <p>Content...</p>
    </section>
  </article>
</main>

<!-- Data tables -->
<table>
  <caption>Quarterly Sales Report</caption>
  <thead>
    <tr>
      <th scope="col">Quarter</th>
      <th scope="col">Revenue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Q1</th>
      <td>$1.2M</td>
    </tr>
  </tbody>
</table>

<!-- Form labels -->
<div class="form-group">
  <label for="email">Email address</label>
  <input type="email" id="email" name="email"
         aria-describedby="email-hint">
  <p id="email-hint">We'll never share your email.</p>
</div>
```

#### 1.4 Distinguishable

```css
/* Color contrast - WCAG AA */
.text-primary {
  color: #1f2937; /* 12.6:1 on white */
}

.text-secondary {
  color: #4b5563; /* 7.5:1 on white */
}

.text-muted {
  color: #6b7280; /* 5.0:1 on white - passes AA */
}

/* Don't rely on color alone */
.error-field {
  border-color: #ef4444;
  border-width: 2px; /* Visual indicator beyond color */
}

.error-field::before {
  content: "⚠ "; /* Icon indicator */
}

/* Focus indicators */
:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Text resize - use relative units */
body {
  font-size: 100%; /* Respect user preferences */
}

h1 {
  font-size: 2.5rem; /* Not px */
}

/* Text spacing - allow customization */
p {
  line-height: 1.5;
  letter-spacing: normal;
  word-spacing: normal;
}
```

### Operable

Users must be able to operate the interface.

#### 2.1 Keyboard Accessible

```html
<!-- All interactive elements are focusable -->
<button>Click me</button>
<a href="/page">Link</a>
<input type="text">
<select>...</select>

<!-- Custom interactive elements -->
<div role="button" tabindex="0"
     onkeydown="handleKeyDown(event)"
     onclick="handleClick()">
  Custom Button
</div>

<!-- Skip links -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>

<main id="main-content" tabindex="-1">
  <!-- Main content -->
</main>
```

```css
/* Skip link styles */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: 8px;
  background: #000;
  color: #fff;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

```javascript
// Keyboard handler for custom elements
function handleKeyDown(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    handleClick();
  }
}
```

#### 2.4 Navigable

```html
<!-- Page title -->
<title>Contact Us | Company Name</title>

<!-- Heading hierarchy -->
<h1>Main Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

<!-- Landmarks -->
<header role="banner">...</header>
<nav role="navigation" aria-label="Main">...</nav>
<main role="main">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>

<!-- Multiple navs need labels -->
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Footer navigation">...</nav>

<!-- Breadcrumbs -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Widget</li>
  </ol>
</nav>
```

#### 2.5 Input Modalities

```css
/* Touch targets - minimum 44x44px */
.btn {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
}

/* Adequate spacing between targets */
.nav-list {
  display: flex;
  gap: 8px;
}

.nav-link {
  padding: 12px 16px;
}

/* Motion preferences */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Understandable

Content must be understandable.

#### 3.1 Readable

```html
<!-- Language declaration -->
<html lang="en">

<!-- Language changes -->
<p>The French word <span lang="fr">bonjour</span> means hello.</p>
```

#### 3.2 Predictable

```html
<!-- Consistent navigation -->
<!-- Keep navigation in same location across pages -->

<!-- No unexpected context changes -->
<select onchange="/* Don't auto-submit */">
  <option>Select an option</option>
</select>

<!-- Warn about new windows -->
<a href="https://external.com" target="_blank"
   rel="noopener noreferrer">
  External Link
  <span class="sr-only">(opens in new tab)</span>
</a>
```

#### 3.3 Input Assistance

```html
<!-- Error identification -->
<div class="form-group" aria-invalid="true">
  <label for="email">Email address</label>
  <input type="email" id="email"
         aria-describedby="email-error"
         aria-invalid="true">
  <p id="email-error" class="error" role="alert">
    Please enter a valid email address
  </p>
</div>

<!-- Labels and instructions -->
<label for="password">
  Password
  <span class="required">(required)</span>
</label>
<input type="password" id="password"
       required
       aria-describedby="password-requirements">
<ul id="password-requirements">
  <li>At least 8 characters</li>
  <li>Include a number</li>
  <li>Include a special character</li>
</ul>

<!-- Error prevention for important actions -->
<form>
  <!-- Confirmation step before delete -->
  <dialog id="confirm-delete">
    <p>Are you sure you want to delete this item?</p>
    <button type="button">Cancel</button>
    <button type="submit">Delete</button>
  </dialog>
</form>
```

### Robust

Content must be compatible with assistive technologies.

```html
<!-- Valid HTML -->
<!-- Use W3C validator: validator.w3.org -->

<!-- Proper ARIA usage -->
<div role="tablist">
  <button role="tab"
          aria-selected="true"
          aria-controls="panel-1"
          id="tab-1">
    Tab 1
  </button>
  <button role="tab"
          aria-selected="false"
          aria-controls="panel-2"
          id="tab-2">
    Tab 2
  </button>
</div>

<div role="tabpanel"
     id="panel-1"
     aria-labelledby="tab-1">
  Panel 1 content
</div>

<div role="tabpanel"
     id="panel-2"
     aria-labelledby="tab-2"
     hidden>
  Panel 2 content
</div>

<!-- Status messages -->
<div role="status" aria-live="polite">
  Form submitted successfully
</div>

<div role="alert" aria-live="assertive">
  Error: Connection lost
</div>
```

---

## Common ARIA Patterns

### Modal Dialog

```html
<dialog id="modal"
        aria-labelledby="modal-title"
        aria-describedby="modal-desc">
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-desc">Are you sure you want to proceed?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</dialog>
```

```javascript
// Modal behavior
const modal = document.getElementById('modal');

function openModal() {
  modal.showModal();
  // Focus first focusable element
  modal.querySelector('button').focus();
}

function closeModal() {
  modal.close();
  // Return focus to trigger
  triggerButton.focus();
}

// Trap focus within modal
modal.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
});
```

### Accordion

```html
<div class="accordion">
  <h3>
    <button aria-expanded="true"
            aria-controls="section1"
            id="accordion1">
      Section 1
    </button>
  </h3>
  <div id="section1"
       role="region"
       aria-labelledby="accordion1">
    Content for section 1
  </div>

  <h3>
    <button aria-expanded="false"
            aria-controls="section2"
            id="accordion2">
      Section 2
    </button>
  </h3>
  <div id="section2"
       role="region"
       aria-labelledby="accordion2"
       hidden>
    Content for section 2
  </div>
</div>
```

### Dropdown Menu

```html
<div class="dropdown">
  <button aria-haspopup="true"
          aria-expanded="false"
          aria-controls="menu1">
    Options
  </button>
  <ul id="menu1" role="menu" hidden>
    <li role="menuitem">
      <button>Edit</button>
    </li>
    <li role="menuitem">
      <button>Delete</button>
    </li>
  </ul>
</div>
```

### Live Regions

```html
<!-- Polite: announced when user is idle -->
<div aria-live="polite" aria-atomic="true">
  3 items in cart
</div>

<!-- Assertive: announced immediately -->
<div aria-live="assertive" role="alert">
  Error: Please check your input
</div>

<!-- Status: for non-critical updates -->
<div role="status">
  Saving...
</div>

<!-- Log: for chat, activity feeds -->
<div role="log" aria-live="polite">
  <!-- New messages appended here -->
</div>
```

---

## Screen Reader Only Content

```css
/* Visually hidden but accessible */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focusable when navigated to */
.sr-only-focusable:focus,
.sr-only-focusable:active {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

```html
<!-- Use cases -->
<a href="/cart">
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Shopping cart</span>
  <span class="badge">3</span>
</a>

<table>
  <caption class="sr-only">User data table</caption>
  ...
</table>
```

---

## Focus Management

```css
/* Visible focus indicators */
:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Remove default, add custom */
button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.5);
}

/* Focus within containers */
.card:focus-within {
  box-shadow: 0 0 0 2px #2563eb;
}
```

```javascript
// Programmatic focus management
function openModal(modal) {
  // Save current focus
  const previousFocus = document.activeElement;

  // Open modal
  modal.showModal();

  // Focus first element
  modal.querySelector('[autofocus]')?.focus();

  // On close, restore focus
  modal.addEventListener('close', () => {
    previousFocus.focus();
  }, { once: true });
}

// Focus trap
function trapFocus(container) {
  const focusable = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  container.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}
```

---

## Testing Checklist

### Automated Testing
- [ ] Run axe DevTools or WAVE
- [ ] Check color contrast with tools
- [ ] Validate HTML

### Keyboard Testing
- [ ] Tab through entire page
- [ ] All interactive elements focusable
- [ ] Focus order makes sense
- [ ] Focus visible at all times
- [ ] Can escape modals/menus
- [ ] No keyboard traps

### Screen Reader Testing
- [ ] Page title announced
- [ ] Headings navigable
- [ ] Landmarks present
- [ ] Images have alt text
- [ ] Forms have labels
- [ ] Errors announced
- [ ] Dynamic content announced

### Visual Testing
- [ ] 200% zoom works
- [ ] Text resize works
- [ ] Color not only indicator
- [ ] Sufficient contrast
- [ ] Reduced motion respected

---

## Common Mistakes to Avoid

1. **Empty links/buttons**: Always have accessible text
2. **Missing form labels**: Every input needs a label
3. **Div/span as buttons**: Use semantic `<button>`
4. **Auto-playing media**: Allow users to stop
5. **Time limits**: Warn users, allow extensions
6. **CAPTCHA without alternative**: Provide audio option
7. **PDF without alternative**: Provide HTML version
8. **Infinite scroll without alternative**: Provide pagination
9. **Custom controls without ARIA**: Add proper roles
10. **Color as only indicator**: Add icons/text

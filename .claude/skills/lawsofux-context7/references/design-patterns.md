# Design Patterns Implementing Laws of UX

Practical patterns and code examples for applying UX laws in your designs.

---

## Navigation Patterns

### Limited Navigation (Hick's Law + Miller's Law)

```html
<nav class="main-nav">
  <a href="/" class="nav-logo">Logo</a>
  <ul class="nav-links">
    <li><a href="/products">Products</a></li>
    <li><a href="/solutions">Solutions</a></li>
    <li><a href="/pricing">Pricing</a></li>
    <li><a href="/resources">Resources</a></li>
    <li><a href="/company">Company</a></li>
  </ul>
  <div class="nav-actions">
    <a href="/login" class="btn-secondary">Log in</a>
    <a href="/signup" class="btn-primary">Get Started</a>
  </div>
</nav>
```

```css
.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  max-width: 1280px;
  margin: 0 auto;
}

.nav-links {
  display: flex;
  gap: 32px;
  list-style: none;
}

.nav-links a {
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 0;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: #3b82f6;
}

/* Max 7 items in primary navigation */
.nav-links li:nth-child(n+8) {
  display: none;
}

/* Mobile: hamburger menu for overflow */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
}
```

---

## Button Patterns

### Touch-Friendly Buttons (Fitts's Law)

```css
/* Base button - meets minimum touch target */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* Primary action - most prominent */
.button-primary {
  background: #3b82f6;
  color: white;
}

.button-primary:hover {
  background: #2563eb;
}

.button-primary:active {
  transform: scale(0.98);
}

/* Increased touch target without visual change */
.icon-button {
  position: relative;
  width: 24px;
  height: 24px;
}

.icon-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
}

/* Full-width CTA on mobile */
@media (max-width: 640px) {
  .button-cta {
    width: 100%;
    padding: 16px;
  }
}
```

### Distinctive Primary Action (Von Restorff Effect)

```css
.button-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.button-secondary {
  background: transparent;
  color: #374151;
  border: 1px solid #d1d5db;
}

.button-secondary:hover {
  background: #f3f4f6;
}

/* Primary stands out through color and weight */
.button-primary {
  background: #3b82f6;
  color: white;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Destructive action - different color family */
.button-danger {
  background: #dc2626;
  color: white;
}
```

---

## Form Patterns

### Progressive Disclosure (Hick's Law + Cognitive Load)

```html
<form class="checkout-form">
  <!-- Step 1: Essential info first -->
  <fieldset class="form-section active">
    <legend>Contact Information</legend>
    <div class="form-field">
      <label for="email">Email</label>
      <input type="email" id="email" required>
    </div>
  </fieldset>

  <!-- Step 2: Revealed after step 1 -->
  <fieldset class="form-section">
    <legend>Shipping Address</legend>
    <!-- More fields -->
  </fieldset>

  <!-- Step 3: Payment last -->
  <fieldset class="form-section">
    <legend>Payment</legend>
    <!-- Payment fields -->
  </fieldset>
</form>
```

```css
.form-section {
  opacity: 0.5;
  pointer-events: none;
  margin-bottom: 24px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

.form-section.active {
  opacity: 1;
  pointer-events: auto;
  border-color: #3b82f6;
}

.form-section.completed {
  opacity: 1;
  background: #f0fdf4;
  border-color: #10b981;
}

/* Tight proximity between label and input */
.form-field {
  margin-bottom: 16px;
}

.form-field label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: #374151;
}

.form-field input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 16px;
}

.form-field input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

### Flexible Input (Postel's Law)

```css
/* Accept various formats */
.phone-input {
  position: relative;
}

.phone-input input {
  padding-left: 80px;
}

.phone-input .country-code {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
}

/* Chunked display for readability */
.card-input {
  letter-spacing: 2px;
  font-family: monospace;
}

/* Format hint */
.form-field .hint {
  margin-top: 4px;
  font-size: 14px;
  color: #6b7280;
}
```

---

## Progress Patterns

### Progress Indicator (Goal-Gradient Effect)

```html
<div class="progress-container">
  <div class="progress-bar">
    <div class="progress-fill" style="width: 65%"></div>
  </div>
  <div class="progress-label">
    <span>Profile completion</span>
    <span>65%</span>
  </div>
</div>
```

```css
.progress-container {
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.progress-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
}

/* Animated fill for engagement */
@keyframes progress-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.progress-fill.active {
  animation: progress-pulse 2s ease infinite;
}
```

### Step Indicator (Zeigarnik Effect)

```html
<div class="steps">
  <div class="step completed">
    <div class="step-icon">✓</div>
    <div class="step-label">Account</div>
  </div>
  <div class="step active">
    <div class="step-icon">2</div>
    <div class="step-label">Profile</div>
  </div>
  <div class="step">
    <div class="step-icon">3</div>
    <div class="step-label">Preferences</div>
  </div>
</div>
```

```css
.steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

/* Connecting line */
.steps::before {
  content: '';
  position: absolute;
  top: 20px;
  left: 10%;
  right: 10%;
  height: 2px;
  background: #e5e7eb;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: #9ca3af;
}

.step.completed .step-icon {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.step.active .step-icon {
  border-color: #3b82f6;
  color: #3b82f6;
}

.step-label {
  margin-top: 8px;
  font-size: 14px;
  color: #6b7280;
}

.step.active .step-label {
  color: #3b82f6;
  font-weight: 500;
}
```

---

## Card Patterns

### Grouped Content (Law of Common Region)

```css
.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
}

.card-content {
  color: #374151;
}

.card-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

/* Card grid with consistent spacing */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}
```

### Featured Card (Von Restorff Effect)

```css
.pricing-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  border: 1px solid #e5e7eb;
  text-align: center;
}

.pricing-card.featured {
  border-color: #3b82f6;
  border-width: 2px;
  transform: scale(1.05);
  box-shadow: 0 20px 40px -12px rgba(59, 130, 246, 0.25);
  position: relative;
}

.pricing-card.featured::before {
  content: 'Most Popular';
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: #3b82f6;
  color: white;
  padding: 4px 16px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
}
```

---

## Feedback Patterns

### Instant Feedback (Doherty Threshold)

```css
/* Button state feedback */
.button {
  transition: all 0.15s ease;
}

.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.button:active {
  transform: translateY(0) scale(0.98);
}

/* Loading state */
.button.loading {
  position: relative;
  color: transparent;
  pointer-events: none;
}

.button.loading::after {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Skeleton loading */
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s ease infinite;
  border-radius: 4px;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Success State (Peak-End Rule)

```css
.success-message {
  text-align: center;
  padding: 48px;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border-radius: 16px;
}

.success-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: celebrate 0.5s ease;
}

@keyframes celebrate {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  70% { transform: scale(0.9); }
  100% { transform: scale(1); }
}

.success-icon svg {
  width: 32px;
  height: 32px;
  color: white;
}

.success-title {
  font-size: 24px;
  font-weight: 600;
  color: #065f46;
  margin-bottom: 8px;
}

.success-message p {
  color: #047857;
}
```

---

## List Patterns

### Prioritized List (Serial Position Effect)

```css
.feature-list {
  list-style: none;
  padding: 0;
}

.feature-list li {
  display: flex;
  align-items: flex-start;
  padding: 16px 0;
  border-bottom: 1px solid #e5e7eb;
}

/* First and last items emphasized */
.feature-list li:first-child,
.feature-list li:last-child {
  font-weight: 500;
}

.feature-list li:first-child::before {
  content: '⭐';
  margin-right: 12px;
}

.feature-list .icon {
  width: 24px;
  height: 24px;
  margin-right: 12px;
  color: #10b981;
}
```

### Chunked List (Miller's Law)

```css
/* Group into categories of 5-7 */
.category-group {
  margin-bottom: 32px;
}

.category-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-item {
  padding: 12px;
  border-radius: 6px;
  transition: background 0.15s;
}

.category-item:hover {
  background: #f3f4f6;
}
```

---

## Responsive Patterns

### Consistent Patterns Across Devices (Jakob's Law)

```css
/* Desktop navigation */
.nav {
  display: flex;
  gap: 24px;
}

/* Mobile: familiar hamburger pattern */
@media (max-width: 768px) {
  .nav {
    display: none;
  }

  .mobile-menu-button {
    display: block;
  }

  .nav.open {
    display: flex;
    flex-direction: column;
    position: fixed;
    inset: 0;
    background: white;
    padding: 80px 24px 24px;
  }
}

/* Touch targets for mobile (Fitts's Law) */
@media (max-width: 768px) {
  .button {
    min-height: 48px;
    padding: 14px 24px;
  }

  .list-item {
    padding: 16px;
  }

  .form-field input {
    padding: 14px;
    font-size: 16px; /* Prevents iOS zoom */
  }
}
```

---

## Summary: Pattern Selection Guide

| User Need | Law | Pattern |
|-----------|-----|---------|
| Quick decisions | Hick's Law | Limited options, smart defaults |
| Easy targeting | Fitts's Law | Large buttons, close grouping |
| Motivation | Goal-Gradient | Progress bars, step indicators |
| Memory limits | Miller's Law | Chunked content, categories |
| Familiarity | Jakob's Law | Standard layouts, conventions |
| Attention | Von Restorff | Highlighted CTAs, badges |
| Grouping | Common Region | Cards, bordered sections |
| Flow state | Doherty Threshold | Instant feedback, skeletons |
| Satisfaction | Peak-End Rule | Celebration states |
| Completion | Zeigarnik Effect | Draft indicators, reminders |

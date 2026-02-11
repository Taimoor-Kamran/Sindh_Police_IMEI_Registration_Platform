# CSS Implementation Patterns

## Component Patterns

### Buttons

```css
/* Base button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.25rem;
  border-radius: 0.5rem;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 150ms ease;
  text-decoration: none;
}

.btn:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Variants */
.btn-primary {
  background: #2563eb;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #1d4ed8;
}

.btn-secondary {
  background: #ffffff;
  color: #374151;
  border-color: #d1d5db;
}

.btn-secondary:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn-ghost {
  background: transparent;
  color: #374151;
}

.btn-ghost:hover:not(:disabled) {
  background: #f3f4f6;
}

.btn-danger {
  background: #dc2626;
  color: #ffffff;
}

.btn-danger:hover:not(:disabled) {
  background: #b91c1c;
}

/* Sizes */
.btn-sm {
  padding: 0.375rem 0.875rem;
  font-size: 0.75rem;
}

.btn-lg {
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
}

/* Icon button */
.btn-icon {
  padding: 0.625rem;
  aspect-ratio: 1;
}
```

### Cards

```css
.card {
  background: #ffffff;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.card-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  background: #f9fafb;
  border-top: 1px solid #e5e7eb;
}

/* Interactive card */
.card-interactive {
  cursor: pointer;
  transition: all 150ms ease;
}

.card-interactive:hover {
  border-color: #9ca3af;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.card-interactive:focus-within {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

/* Card with image */
.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

### Form Inputs

```css
/* Input base */
.input {
  display: block;
  width: 100%;
  padding: 0.625rem 0.875rem;
  font-size: 0.875rem;
  line-height: 1.25rem;
  color: #111827;
  background: #ffffff;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  transition: all 150ms ease;
}

.input::placeholder {
  color: #9ca3af;
}

.input:hover:not(:disabled) {
  border-color: #9ca3af;
}

.input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1);
}

.input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

/* Error state */
.input-error {
  border-color: #dc2626;
}

.input-error:focus {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgb(220 38 38 / 0.1);
}

/* Form group */
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-helper {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #6b7280;
}

.form-error {
  margin-top: 0.375rem;
  font-size: 0.75rem;
  color: #dc2626;
}

/* Checkbox & Radio */
.checkbox,
.radio {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox input,
.radio input {
  width: 1rem;
  height: 1rem;
  cursor: pointer;
  accent-color: #2563eb;
}

/* Select */
.select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3E%3C/svg%3E");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

/* Textarea */
.textarea {
  min-height: 6rem;
  resize: vertical;
}
```

### Navigation

```css
/* Navbar */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.navbar-brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  text-decoration: none;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  color: #4b5563;
  text-decoration: none;
  border-radius: 0.375rem;
  transition: all 150ms ease;
}

.nav-link:hover {
  color: #111827;
  background: #f3f4f6;
}

.nav-link.active {
  color: #2563eb;
  font-weight: 500;
}

/* Mobile nav toggle */
.nav-toggle {
  display: none;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
}

@media (max-width: 768px) {
  .nav-toggle {
    display: block;
  }

  .navbar-nav {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    flex-direction: column;
    padding: 1rem;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
  }

  .navbar-nav.open {
    display: flex;
  }
}

/* Breadcrumbs */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.breadcrumb-item a {
  color: #4b5563;
  text-decoration: none;
}

.breadcrumb-item a:hover {
  color: #2563eb;
  text-decoration: underline;
}

.breadcrumb-separator {
  color: #d1d5db;
}

.breadcrumb-current {
  color: #111827;
  font-weight: 500;
}
```

### Modal/Dialog

```css
/* Backdrop */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgb(0 0 0 / 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 50;
}

/* Modal */
.modal {
  background: #ffffff;
  border-radius: 0.75rem;
  max-width: 32rem;
  width: 100%;
  max-height: calc(100vh - 2rem);
  overflow: auto;
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  padding: 0.25rem;
  color: #6b7280;
  background: none;
  border: none;
  border-radius: 0.375rem;
  cursor: pointer;
}

.modal-close:hover {
  color: #111827;
  background: #f3f4f6;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

/* Native dialog */
dialog {
  border: none;
  border-radius: 0.75rem;
  padding: 0;
  max-width: 32rem;
  width: calc(100% - 2rem);
}

dialog::backdrop {
  background: rgb(0 0 0 / 0.5);
}
```

### Alerts/Notifications

```css
.alert {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.alert-icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.alert-info {
  background: #eff6ff;
  color: #1e40af;
  border: 1px solid #bfdbfe;
}

.alert-success {
  background: #f0fdf4;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.alert-warning {
  background: #fffbeb;
  color: #92400e;
  border: 1px solid #fde68a;
}

.alert-error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

/* Toast notifications */
.toast-container {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 100;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: #1f2937;
  color: #ffffff;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  animation: slide-in 200ms ease;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

### Tabs

```css
.tabs {
  border-bottom: 1px solid #e5e7eb;
}

.tab-list {
  display: flex;
  gap: 0;
  margin: 0;
  padding: 0;
  list-style: none;
}

.tab {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #6b7280;
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  cursor: pointer;
  transition: all 150ms ease;
}

.tab:hover {
  color: #374151;
}

.tab[aria-selected="true"],
.tab.active {
  color: #2563eb;
  border-bottom-color: #2563eb;
}

.tab:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: -2px;
}

.tab-panel {
  padding: 1.5rem 0;
}

.tab-panel[hidden] {
  display: none;
}
```

---

## Layout Patterns

### Container

```css
.container {
  width: 100%;
  max-width: 1280px;
  margin-inline: auto;
  padding-inline: 1rem;
}

@media (min-width: 640px) {
  .container {
    padding-inline: 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding-inline: 2rem;
  }
}

/* Prose container for content */
.prose {
  max-width: 65ch;
}
```

### Stack (Vertical)

```css
.stack {
  display: flex;
  flex-direction: column;
}

.stack > * + * {
  margin-top: var(--stack-gap, 1rem);
}

/* Variants */
.stack-xs { --stack-gap: 0.25rem; }
.stack-sm { --stack-gap: 0.5rem; }
.stack-md { --stack-gap: 1rem; }
.stack-lg { --stack-gap: 1.5rem; }
.stack-xl { --stack-gap: 2rem; }
```

### Cluster (Horizontal)

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--cluster-gap, 1rem);
  align-items: center;
}

/* Variants */
.cluster-xs { --cluster-gap: 0.25rem; }
.cluster-sm { --cluster-gap: 0.5rem; }
.cluster-md { --cluster-gap: 1rem; }
.cluster-lg { --cluster-gap: 1.5rem; }
```

### Sidebar Layout

```css
.sidebar-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

.sidebar-layout > :first-child {
  flex-basis: 280px;
  flex-grow: 1;
}

.sidebar-layout > :last-child {
  flex-basis: 0;
  flex-grow: 999;
  min-width: 60%;
}
```

### Grid Auto-Fill

```css
.grid-auto {
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(min(300px, 100%), 1fr)
  );
  gap: 1.5rem;
}
```

### Center

```css
/* Horizontal center */
.center-h {
  margin-inline: auto;
  width: fit-content;
}

/* Vertical center */
.center-v {
  display: flex;
  align-items: center;
  min-height: 100%;
}

/* Both */
.center {
  display: grid;
  place-items: center;
}
```

### Cover (Full Height)

```css
.cover {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.cover > :first-child {
  margin-top: 0;
}

.cover > :last-child {
  margin-bottom: 0;
}

.cover > .center {
  margin-block: auto;
}
```

---

## Animation Patterns

### Transitions

```css
/* Base transition */
.transition {
  transition: all 150ms ease;
}

/* Specific properties */
.transition-colors {
  transition: color, background-color, border-color 150ms ease;
}

.transition-transform {
  transition: transform 200ms ease;
}

.transition-opacity {
  transition: opacity 200ms ease;
}

/* Duration variants */
.duration-75 { transition-duration: 75ms; }
.duration-100 { transition-duration: 100ms; }
.duration-150 { transition-duration: 150ms; }
.duration-200 { transition-duration: 200ms; }
.duration-300 { transition-duration: 300ms; }
```

### Keyframe Animations

```css
/* Fade in */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-fade-in {
  animation: fade-in 200ms ease;
}

/* Slide up */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 200ms ease;
}

/* Scale */
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 200ms ease;
}

/* Spin */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s ease-in-out infinite;
}

/* Bounce */
@keyframes bounce {
  0%, 100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Loading States

### Spinner

```css
.spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

.spinner-sm {
  width: 1rem;
  height: 1rem;
}

.spinner-lg {
  width: 2rem;
  height: 2rem;
}
```

### Skeleton

```css
.skeleton {
  background: linear-gradient(
    90deg,
    #e5e7eb 25%,
    #f3f4f6 50%,
    #e5e7eb 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 0.25rem;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton-text {
  height: 1rem;
  margin-bottom: 0.5rem;
}

.skeleton-heading {
  height: 1.5rem;
  width: 60%;
  margin-bottom: 1rem;
}

.skeleton-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
}

.skeleton-image {
  width: 100%;
  aspect-ratio: 16 / 9;
}
```

### Progress Bar

```css
.progress {
  width: 100%;
  height: 0.5rem;
  background: #e5e7eb;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: #2563eb;
  border-radius: 9999px;
  transition: width 200ms ease;
}

/* Indeterminate */
.progress-indeterminate .progress-bar {
  width: 30%;
  animation: progress-indeterminate 1.5s infinite;
}

@keyframes progress-indeterminate {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
```

---

## Utility Classes

### Display

```css
.hidden { display: none; }
.block { display: block; }
.inline { display: inline; }
.inline-block { display: inline-block; }
.flex { display: flex; }
.inline-flex { display: inline-flex; }
.grid { display: grid; }
```

### Flexbox

```css
.flex-row { flex-direction: row; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.flex-nowrap { flex-wrap: nowrap; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }

.flex-1 { flex: 1 1 0%; }
.flex-auto { flex: 1 1 auto; }
.flex-none { flex: none; }
```

### Spacing

```css
/* Margin */
.m-0 { margin: 0; }
.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-4 { margin: 1rem; }
.m-auto { margin: auto; }

.mx-auto { margin-inline: auto; }
.my-4 { margin-block: 1rem; }

/* Padding */
.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-4 { padding: 1rem; }

/* Gap */
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
```

### Typography

```css
.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }

.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

.text-left { text-align: left; }
.text-center { text-align: center; }
.text-right { text-align: right; }

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### Colors

```css
.text-primary { color: #111827; }
.text-secondary { color: #4b5563; }
.text-muted { color: #6b7280; }
.text-white { color: #ffffff; }

.bg-white { background: #ffffff; }
.bg-gray-50 { background: #f9fafb; }
.bg-gray-100 { background: #f3f4f6; }
.bg-primary { background: #2563eb; }

.border-gray-200 { border-color: #e5e7eb; }
.border-gray-300 { border-color: #d1d5db; }
```

### Border Radius

```css
.rounded-none { border-radius: 0; }
.rounded-sm { border-radius: 0.125rem; }
.rounded { border-radius: 0.25rem; }
.rounded-md { border-radius: 0.375rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-xl { border-radius: 0.75rem; }
.rounded-2xl { border-radius: 1rem; }
.rounded-full { border-radius: 9999px; }
```

### Shadow

```css
.shadow-sm { box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
.shadow { box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1); }
.shadow-md { box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }
.shadow-lg { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); }
.shadow-xl { box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); }
```

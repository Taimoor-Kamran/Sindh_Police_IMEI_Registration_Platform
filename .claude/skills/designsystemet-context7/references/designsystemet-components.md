# Designsystemet Component Reference

Quick reference for Designsystemet components and patterns.

## Installation

```bash
npm install @digdir/designsystemet-css @digdir/designsystemet-theme @digdir/designsystemet-react
```

## Core Components

### Button

```tsx
import { Button } from '@digdir/designsystemet-react';

// Variants
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="tertiary">Tertiary</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>

// With icon
<Button icon={<Icon />}>With Icon</Button>
```

### Alert

```tsx
import { Alert } from '@digdir/designsystemet-react';

<Alert severity="info">Information message</Alert>
<Alert severity="warning">Warning message</Alert>
<Alert severity="success">Success message</Alert>
<Alert severity="danger">Error message</Alert>
```

### Textfield

```tsx
import { Textfield } from '@digdir/designsystemet-react';

<Textfield
  label="Email"
  description="Enter your email address"
  error="Invalid email format"
/>
```

### Accordion

```tsx
import { Accordion } from '@digdir/designsystemet-react';

<Accordion>
  <Accordion.Item>
    <Accordion.Heading>Section 1</Accordion.Heading>
    <Accordion.Content>Content here</Accordion.Content>
  </Accordion.Item>
</Accordion>
```

### Tabs

```tsx
import { Tabs } from '@digdir/designsystemet-react';

<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
  <Tabs.Content value="tab1">Content 1</Tabs.Content>
  <Tabs.Content value="tab2">Content 2</Tabs.Content>
</Tabs>
```

### Checkbox

```tsx
import { Checkbox } from '@digdir/designsystemet-react';

<Checkbox label="Accept terms" />
<Checkbox label="Disabled" disabled />
<Checkbox label="Checked" checked />
```

### Radio

```tsx
import { Radio } from '@digdir/designsystemet-react';

<Radio.Group legend="Choose option">
  <Radio value="1" label="Option 1" />
  <Radio value="2" label="Option 2" />
  <Radio value="3" label="Option 3" />
</Radio.Group>
```

### Select

```tsx
import { Select } from '@digdir/designsystemet-react';

<Select label="Choose country">
  <Select.Option value="no">Norway</Select.Option>
  <Select.Option value="se">Sweden</Select.Option>
  <Select.Option value="dk">Denmark</Select.Option>
</Select>
```

## Form Patterns

### Form with Validation

```tsx
import { Textfield, Button, Alert } from '@digdir/designsystemet-react';

<form>
  <Textfield
    label="Name"
    required
    error={errors.name}
  />
  <Textfield
    label="Email"
    type="email"
    required
    error={errors.email}
  />
  <Button type="submit" variant="primary">
    Submit
  </Button>
</form>
```

## Theming

### Using Default Theme

```tsx
import '@digdir/designsystemet-theme';
import '@digdir/designsystemet-css';
```

### Custom Theme

Use the theme builder at https://theme.designsystemet.no/ to create custom themes.

## Accessibility

All components follow WCAG 2.1 AA guidelines:

- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Sufficient color contrast
- Proper ARIA attributes

### Common A11y Props

```tsx
// Add accessible label
<Button aria-label="Close dialog">X</Button>

// Link to description
<Textfield aria-describedby="helper-text" />

// Required field
<Textfield required aria-required="true" />
```

## Design Tokens

### Colors

- `--ds-color-accent-*` - Primary accent colors
- `--ds-color-neutral-*` - Neutral grays
- `--ds-color-success-*` - Success states
- `--ds-color-warning-*` - Warning states
- `--ds-color-danger-*` - Error states

### Spacing

- `--ds-spacing-1` through `--ds-spacing-12`

### Typography

- `--ds-font-size-*` - Font sizes
- `--ds-font-weight-*` - Font weights
- `--ds-line-height-*` - Line heights

## Resources

- [Documentation](https://designsystemet.no/en/)
- [GitHub](https://github.com/digdir/designsystemet)
- [Theme Builder](https://theme.designsystemet.no/)
- [Storybook](https://storybook.designsystemet.no/)

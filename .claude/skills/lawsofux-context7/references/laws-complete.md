# Laws of UX Complete Reference

A comprehensive guide to psychological principles that inform user experience design.

---

## Aesthetic-Usability Effect

### Definition
Users often perceive aesthetically pleasing design as design that's more usable.

### Psychological Basis
- Positive emotional response creates a halo effect
- Attractive things work better (Don Norman)
- People are more tolerant of minor usability issues when design is visually appealing

### Key Takeaways
- Aesthetically pleasing design creates positive response and perceived usability
- Users are more forgiving of minor usability issues with beautiful interfaces
- Visual design matters as much as functionality

### Implementation
```css
/* Create visual harmony with consistent spacing and typography */
.card {
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### Examples
- Apple's product pages combine beauty with usability
- Stripe's documentation is both beautiful and functional
- Notion's clean interface makes complex features feel simple

---

## Doherty Threshold

### Definition
Productivity soars when a computer and its users interact at a pace (<400ms) that ensures neither has to wait on the other.

### Psychological Basis
- Named after Walter Doherty's 1982 IBM research
- Response times under 400ms keep users in a "flow" state
- Delays over 1 second break user concentration

### Key Takeaways
- Provide system feedback within 400ms
- Use progress indicators for longer operations
- Optimize perceived performance with instant UI updates

### Implementation
```css
/* Instant feedback on interaction */
.button {
  transition: background-color 0.1s ease, transform 0.1s ease;
}

.button:active {
  transform: scale(0.98);
}

/* Skeleton loading for perceived speed */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Response Time Guidelines
| Time | Perception | Action |
|------|------------|--------|
| <100ms | Instantaneous | No feedback needed |
| 100-400ms | Slight delay | Simple transition |
| 400ms-1s | Noticeable | Show loading indicator |
| 1-10s | Long wait | Progress bar + explanation |
| >10s | Too long | Allow background operation |

---

## Fitts's Law

### Definition
The time to acquire a target is a function of the distance to and size of the target.

### Psychological Basis
- Formulated by Paul Fitts in 1954
- Mathematical model: T = a + b * log2(D/W + 1)
- Where T=time, D=distance, W=width of target

### Key Takeaways
- Make clickable elements large enough to be easily selectable
- Place important actions within easy reach
- Reduce distance between related actions

### Implementation
```css
/* Touch-friendly button sizes */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
}

/* Large click targets with padding */
.nav-link {
  display: block;
  padding: 16px 24px;
}

/* Floating action button - always accessible */
.fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
}

/* Full-width buttons on mobile */
@media (max-width: 640px) {
  .primary-cta {
    width: 100%;
    padding: 16px;
  }
}
```

### Target Size Guidelines
| Device | Minimum | Recommended | Comfortable |
|--------|---------|-------------|-------------|
| Touch (Mobile) | 44×44px | 48×48px | 60×60px |
| Touch (Tablet) | 44×44px | 48×48px | 56×56px |
| Mouse (Desktop) | 24×24px | 32×32px | 44×44px |

---

## Goal-Gradient Effect

### Definition
The tendency to approach a goal increases with proximity to the goal.

### Psychological Basis
- First observed in rats approaching food (Hull, 1932)
- Motivation increases as people get closer to completing a goal
- The "endowed progress effect" - artificial advancement increases completion

### Key Takeaways
- Show users their progress toward completion
- Start progress bars slightly filled (10-20%)
- Break large goals into smaller milestones

### Implementation
```css
/* Progress indicator */
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  transition: width 0.3s ease;
}

/* Step indicator */
.steps {
  display: flex;
  justify-content: space-between;
}

.step {
  flex: 1;
  text-align: center;
  position: relative;
}

.step.completed::before {
  content: '✓';
  color: #10b981;
}
```

### Examples
- Coffee shop loyalty cards (10 stamps, start with 2 free)
- LinkedIn profile completion percentage
- Duolingo's streak and level systems

---

## Hick's Law

### Definition
The time it takes to make a decision increases with the number and complexity of choices.

### Psychological Basis
- Formulated by William Edmund Hick and Ray Hyman
- Mathematical: RT = a + b * log2(n)
- Where RT=reaction time, n=number of choices

### Key Takeaways
- Minimize choices when response times are critical
- Break complex tasks into smaller steps
- Highlight recommended options

### Implementation
```css
/* Highlight primary choice */
.option-group {
  display: flex;
  gap: 16px;
}

.option {
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
}

.option.recommended {
  border-color: #3b82f6;
  position: relative;
}

.option.recommended::before {
  content: 'Recommended';
  position: absolute;
  top: -12px;
  left: 16px;
  background: #3b82f6;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}
```

### Guidelines
- **Navigation**: 5-7 main menu items maximum
- **Forms**: Progressive disclosure for complex forms
- **Pricing**: 3 tiers with one highlighted as "best value"
- **Search**: Provide smart defaults and filters

---

## Jakob's Law

### Definition
Users spend most of their time on other sites. This means that users prefer your site to work the same way as all the other sites they already know.

### Psychological Basis
- Mental models transfer between similar experiences
- Familiarity reduces cognitive load
- Convention over innovation for core interactions

### Key Takeaways
- Use familiar patterns and conventions
- Leverage existing mental models
- Minimize learning curve by building on expectations

### Implementation
```css
/* Standard navigation placement */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}

.logo {
  /* Logo on the left */
}

.nav {
  /* Navigation in center or right */
}

.actions {
  /* Login/CTA on the right */
}

/* Standard form patterns */
.form-field {
  margin-bottom: 24px;
}

.form-field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-field input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
}
```

### Common Conventions
- Logo links to homepage (top left)
- Search in header (often top right)
- Shopping cart icon (top right)
- Footer contains legal/contact info
- Underlined text = link

---

## Law of Common Region

### Definition
Elements tend to be perceived into groups if they are sharing an area with a clearly defined boundary.

### Psychological Basis
- Part of Gestalt psychology principles
- Visual boundaries create perceived groupings
- Stronger than proximity in some contexts

### Key Takeaways
- Use cards, borders, or backgrounds to group related content
- Create clear visual containers for related elements
- Separate unrelated content with whitespace or dividers

### Implementation
```css
/* Card container grouping */
.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Section with background */
.feature-section {
  background: #f9fafb;
  padding: 48px 24px;
  margin: 48px 0;
}

/* Grouped form fields */
.field-group {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.field-group legend {
  padding: 0 8px;
  font-weight: 600;
}
```

---

## Law of Proximity

### Definition
Objects that are near, or proximate to each other, tend to be grouped together.

### Psychological Basis
- Fundamental Gestalt principle
- Brain groups nearby elements automatically
- Spatial relationships convey meaning

### Key Takeaways
- Place related elements close together
- Use whitespace to separate distinct groups
- Spacing should reflect relationships

### Implementation
```css
/* Tight spacing for related items */
.form-group {
  margin-bottom: 24px;
}

.form-group label {
  margin-bottom: 4px; /* Close to input */
}

.form-group .helper-text {
  margin-top: 4px; /* Close to input */
  color: #6b7280;
}

/* More space between groups */
.section + .section {
  margin-top: 48px;
}

/* Related action buttons */
.button-group {
  display: flex;
  gap: 8px; /* Tight grouping */
}

.button-group + .secondary-actions {
  margin-top: 24px; /* Separate from primary */
}
```

---

## Law of Prägnanz

### Definition
People will perceive and interpret ambiguous or complex images as the simplest form possible.

### Psychological Basis
- Also called the Law of Simplicity
- Brain seeks to reduce cognitive effort
- Complex shapes resolved into simple primitives

### Key Takeaways
- Simplify design to essential elements
- Use clear, recognizable shapes and icons
- Avoid unnecessary visual complexity

### Implementation
```css
/* Clean, simple shapes */
.icon {
  /* Use simple geometric shapes */
  border-radius: 50%; /* Circle */
  /* or */
  border-radius: 8px; /* Rounded rectangle */
}

/* Clear visual hierarchy */
.heading {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.subheading {
  font-size: 1.25rem;
  font-weight: 500;
  color: #6b7280;
}

/* Minimal design */
.minimal-card {
  background: white;
  padding: 24px;
  /* No shadows, borders, or decorations */
}
```

---

## Law of Similarity

### Definition
The human eye tends to perceive similar elements in a design as a complete picture, shape, or group.

### Psychological Basis
- Gestalt principle of similarity
- Similar elements (color, shape, size) perceived as related
- Difference signals change in function

### Key Takeaways
- Use consistent styling for elements with similar functions
- Differentiate elements with different purposes
- Color and shape are primary similarity cues

### Implementation
```css
/* Consistent button styles by function */
.button-primary {
  background: #3b82f6;
  color: white;
  border-radius: 6px;
}

.button-secondary {
  background: transparent;
  color: #3b82f6;
  border: 1px solid #3b82f6;
  border-radius: 6px;
}

.button-danger {
  background: #ef4444;
  color: white;
  border-radius: 6px;
}

/* Similar list items */
.list-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.list-item .icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}
```

---

## Law of Uniform Connectedness

### Definition
Elements that are visually connected are perceived as more related than elements with no connection.

### Psychological Basis
- Lines, borders, and visual connectors create groupings
- Connection overrides proximity in some cases
- Visual linking implies relationship

### Key Takeaways
- Use lines or connectors to show relationships
- Connect related elements with visual treatments
- Use consistent connection styles

### Implementation
```css
/* Timeline with connectors */
.timeline-item {
  position: relative;
  padding-left: 32px;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #e5e7eb;
}

.timeline-item::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 8px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #3b82f6;
}

/* Tab indicator showing connection */
.tabs {
  position: relative;
  border-bottom: 2px solid #e5e7eb;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #3b82f6;
}
```

---

## Miller's Law

### Definition
The average person can only keep 7 (plus or minus 2) items in their working memory.

### Psychological Basis
- George Miller's 1956 paper "The Magical Number Seven"
- Working memory has limited capacity
- Chunking helps extend effective capacity

### Key Takeaways
- Don't overload users with too much information at once
- Chunk content into digestible pieces
- Use progressive disclosure for complex information

### Implementation
```css
/* Chunked phone number input */
.phone-input {
  display: flex;
  gap: 8px;
}

.phone-input input {
  text-align: center;
}

.phone-input .area-code { width: 60px; }
.phone-input .prefix { width: 60px; }
.phone-input .line { width: 80px; }

/* Card number in groups */
.card-number {
  letter-spacing: 4px;
}

/* Navigation limit */
.main-nav {
  display: flex;
  gap: 24px;
}

/* Max 7 items recommended */
.main-nav .nav-item:nth-child(n+8) {
  /* Consider moving to "More" dropdown */
}
```

### Chunking Guidelines
| Content Type | Chunk Size | Example |
|-------------|------------|---------|
| Phone numbers | 3-4 digits | (555) 123-4567 |
| Credit cards | 4 digits | 4532 1234 5678 9012 |
| Dates | 2-4 chars | 12/25/2024 |
| Nav items | 5-7 items | Home, About, Services... |
| List items | 5-9 items | Before needing subgroups |

---

## Occam's Razor

### Definition
Among competing hypotheses that predict equally well, the one with the fewest assumptions should be selected.

### Psychological Basis
- Principle of parsimony
- Simple solutions are easier to understand and use
- Complexity should only exist when necessary

### Key Takeaways
- Analyze and remove unnecessary elements
- Don't add features unless truly needed
- Simplicity improves usability

### Implementation
```css
/* Simple form - only essential fields */
.signup-form {
  max-width: 400px;
}

.signup-form .field {
  margin-bottom: 16px;
}

/* Only email and password for signup */
/* Additional info collected later */

/* Clean interface */
.toolbar {
  display: flex;
  gap: 8px;
}

.toolbar button {
  padding: 8px;
  background: transparent;
  border: none;
  border-radius: 4px;
}

/* Only show commonly used actions */
/* Advanced actions in menu */
```

---

## Pareto Principle

### Definition
The Pareto principle states that, for many events, roughly 80% of the effects come from 20% of the causes.

### Psychological Basis
- Named after economist Vilfredo Pareto
- Also known as the 80/20 rule
- Small inputs often produce large outputs

### Key Takeaways
- Focus resources on the most impactful features
- Identify and optimize the critical 20%
- Don't over-invest in rarely used features

### Examples
- 20% of features satisfy 80% of user needs
- 20% of bugs cause 80% of problems
- 20% of users generate 80% of support tickets

---

## Parkinson's Law

### Definition
Any task will inflate until all of the available time is spent.

### Psychological Basis
- Work expands to fill time available
- Constraints force focus and efficiency
- Deadlines create urgency

### Key Takeaways
- Set clear expectations for task completion
- Use time limits and deadlines effectively
- Reduce complexity to reduce time needed

### Examples
- Limited-time offers create urgency
- Countdown timers in checkout
- Auto-save reduces save decision time

---

## Peak-End Rule

### Definition
People judge an experience largely based on how they felt at its peak and at its end, rather than the average of every moment.

### Psychological Basis
- Research by Daniel Kahneman
- Memory prioritizes intense moments and endings
- Duration neglect - length matters less than peaks

### Key Takeaways
- Pay attention to high-points and endings
- Improve the moments that matter most
- End experiences on a positive note

### Implementation
```css
/* Celebratory completion state */
.success-message {
  text-align: center;
  padding: 48px;
}

.success-message .icon {
  font-size: 64px;
  color: #10b981;
  animation: celebrate 0.5s ease;
}

@keyframes celebrate {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.success-message h2 {
  font-size: 24px;
  margin-top: 16px;
}

/* Positive confirmation */
.order-complete {
  background: linear-gradient(135deg, #10b981, #3b82f6);
  color: white;
  padding: 32px;
  border-radius: 12px;
}
```

---

## Postel's Law

### Definition
Be liberal in what you accept, and conservative in what you send.

### Psychological Basis
- Also known as the Robustness Principle
- Originally from TCP/IP specification
- Applies to all interfaces

### Key Takeaways
- Accept various input formats from users
- Provide clear, unambiguous output
- Be forgiving of user mistakes

### Implementation
```javascript
// Accept flexible phone input
function normalizePhone(input) {
  // Accept: (555) 123-4567, 555.123.4567, 5551234567
  return input.replace(/\D/g, '').slice(-10);
}

// Accept flexible date input
function normalizeDate(input) {
  // Accept: 12/25/24, 2024-12-25, Dec 25 2024
  return new Date(input);
}
```

```css
/* Flexible input display */
.search-input {
  /* Accept any case, trim whitespace */
}

.email-input {
  text-transform: lowercase;
}
```

---

## Serial Position Effect

### Definition
Users have a propensity to best remember the first and last items in a series.

### Psychological Basis
- Primacy effect - first items remembered well
- Recency effect - last items remembered well
- Middle items forgotten more easily

### Key Takeaways
- Place important items at beginning and end
- Key actions in first and last positions
- Less critical items in the middle

### Implementation
```css
/* Navigation prioritization */
.main-nav {
  display: flex;
  justify-content: space-between;
}

.nav-primary {
  /* First items - most important */
}

.nav-secondary {
  /* Middle items */
}

.nav-cta {
  /* Last item - key action */
}

/* List structure */
.feature-list {
  /* Best feature first */
  /* Less impressive features middle */
  /* Strong closing feature last */
}
```

---

## Tesler's Law

### Definition
Tesler's Law, also known as The Law of Conservation of Complexity, states that for any system there is a certain amount of complexity which cannot be reduced.

### Psychological Basis
- Named after Larry Tesler
- Complexity must exist somewhere
- Design choice: user bears it or system does

### Key Takeaways
- Ensure burden is on system, not user when possible
- Accept that some complexity is inherent
- Make trade-offs explicit

### Examples
- Email threading hides complexity from users
- Smart defaults reduce decisions
- Auto-complete predicts user intent

---

## Von Restorff Effect

### Definition
The Von Restorff effect, also known as The Isolation Effect, predicts that when multiple similar objects are present, the one that differs from the rest is most likely to be remembered.

### Psychological Basis
- Named after psychiatrist Hedwig von Restorff
- Distinctive items capture attention
- Isolation creates memorability

### Key Takeaways
- Make important actions visually distinctive
- Use contrast to highlight key information
- Don't make everything stand out

### Implementation
```css
/* Distinctive primary CTA */
.button-group {
  display: flex;
  gap: 12px;
}

.button {
  padding: 12px 24px;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  background: white;
}

.button.primary {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
  font-weight: 600;
}

/* Highlighted pricing tier */
.pricing-card.featured {
  transform: scale(1.05);
  border: 2px solid #3b82f6;
  box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.2);
}

/* Sale badge */
.product-card .sale-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: #ef4444;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
}
```

---

## Zeigarnik Effect

### Definition
People remember uncompleted or interrupted tasks better than completed tasks.

### Psychological Basis
- Named after Bluma Zeigarnik
- Incomplete tasks create psychological tension
- Brain keeps incomplete items in working memory

### Key Takeaways
- Use progress indicators to show incomplete status
- Provide clear "save and continue" options
- Remind users of incomplete tasks

### Implementation
```css
/* Profile completion indicator */
.profile-completion {
  background: #f3f4f6;
  padding: 16px;
  border-radius: 8px;
}

.completion-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.completion-fill {
  height: 100%;
  background: #3b82f6;
  transition: width 0.3s;
}

.completion-text {
  margin-top: 8px;
  color: #6b7280;
}

/* Incomplete task indicator */
.task.incomplete {
  border-left: 3px solid #f59e0b;
}

/* Draft indicator */
.document.draft::before {
  content: 'Draft';
  background: #f59e0b;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
```

---

## Quick Reference Summary

### By Category

**Memory & Cognition**
- Miller's Law: 7±2 items in working memory
- Hick's Law: More choices = longer decisions
- Serial Position Effect: Remember first/last best

**Attention & Perception**
- Von Restorff Effect: Distinctive items remembered
- Law of Prägnanz: Simplest interpretation preferred
- Aesthetic-Usability Effect: Beauty = perceived usability

**Motor & Interaction**
- Fitts's Law: Bigger targets, shorter distances = faster
- Doherty Threshold: <400ms response time for flow

**Behavior & Motivation**
- Goal-Gradient Effect: Motivation increases near completion
- Zeigarnik Effect: Incomplete tasks stay in memory
- Peak-End Rule: Endings and peaks matter most

**Gestalt Grouping**
- Proximity: Near = related
- Similarity: Same = related
- Common Region: Contained = related
- Uniform Connectedness: Connected = related

**Design Philosophy**
- Jakob's Law: Leverage familiarity
- Tesler's Law: Complexity is constant
- Occam's Razor: Simpler is better
- Postel's Law: Flexible input, clear output

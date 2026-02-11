# Psychology Principles for UX Design

Underlying cognitive psychology principles that inform the Laws of UX.

---

## Cognitive Load Theory

### Types of Cognitive Load

1. **Intrinsic Load** - Inherent difficulty of the material
2. **Extraneous Load** - Poor design increasing difficulty
3. **Germane Load** - Mental effort for learning/understanding

### Design Implications
- Minimize extraneous load through good design
- Match intrinsic load to user expertise level
- Support germane load with clear mental models

### Reducing Cognitive Load
```css
/* Progressive disclosure */
.accordion-content {
  display: none;
}

.accordion.open .accordion-content {
  display: block;
}

/* Visual hierarchy reduces scanning effort */
.content h1 { font-size: 2.5rem; font-weight: 700; }
.content h2 { font-size: 1.75rem; font-weight: 600; }
.content p { font-size: 1rem; line-height: 1.6; }
```

---

## Working Memory

### Characteristics
- Limited capacity (7±2 items)
- Short duration (15-30 seconds without rehearsal)
- Easily disrupted by interruptions

### Design Implications
- Chunk information into digestible pieces
- Provide external memory aids (progress indicators, breadcrumbs)
- Avoid interrupting user flow

### Chunking Strategies
| Content | Chunk Strategy |
|---------|---------------|
| Phone numbers | (555) 123-4567 |
| Credit cards | 4532 1234 5678 9012 |
| Long text | Paragraphs with headings |
| Steps | Numbered lists |
| Options | Grouped categories |

---

## Attention

### Types of Attention

1. **Selective Attention** - Focusing on specific stimuli
2. **Divided Attention** - Multitasking
3. **Sustained Attention** - Concentration over time

### Design Implications
- Guide attention with visual hierarchy
- Avoid competing for attention (banner blindness)
- Support focused and scanning behaviors

### Visual Attention Patterns
```css
/* F-pattern for text-heavy content */
.content {
  /* Key info in first lines */
  /* Important words at line starts */
}

/* Z-pattern for landing pages */
.hero {
  /* Logo top-left */
  /* CTA top-right or bottom-right */
}

/* Focus attention with contrast */
.highlight {
  background: #fef3c7;
  padding: 2px 4px;
}
```

---

## Mental Models

### Definition
Internal representations of how something works, based on prior experience.

### Design Implications
- Match user expectations from similar products
- Use familiar patterns and metaphors
- Provide clear feedback to update mental models

### Building Mental Models
- Consistent navigation structure
- Predictable interaction patterns
- Clear system status feedback
- Undo/redo support for exploration

---

## Decision Making

### Heuristics & Biases

1. **Anchoring** - First information influences decisions
2. **Availability** - Easily recalled examples seem more common
3. **Confirmation Bias** - Seeking confirming information
4. **Default Effect** - Sticking with defaults

### Design Implications
- Use smart defaults (Default Effect)
- Show relevant examples first (Anchoring)
- Make important options salient (Availability)
- Support informed decisions with clear information

---

## Gestalt Principles

### Core Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| Proximity | Near = grouped | Form labels close to inputs |
| Similarity | Same = grouped | All links same color |
| Continuity | Lines followed | Timeline designs |
| Closure | Gaps completed | Logo icons |
| Figure-Ground | Foreground/background | Modal dialogs |
| Common Fate | Moving together = grouped | Animations |

### Application in UI
```css
/* Proximity - label close to input */
.form-group label {
  margin-bottom: 4px;
}

/* Similarity - consistent button styles */
.button-secondary {
  border: 1px solid currentColor;
  background: transparent;
}

/* Figure-Ground - modal overlay */
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
}

.modal {
  background: white;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}
```

---

## Emotion & Design

### Emotional Design Levels (Don Norman)

1. **Visceral** - Immediate, instinctive reactions
2. **Behavioral** - Usability and function
3. **Reflective** - Long-term impact and memory

### Design Implications
- Create positive first impressions (visceral)
- Ensure smooth, satisfying interactions (behavioral)
- Build meaning and identity (reflective)

### Emotional Responses
```css
/* Positive feedback - success */
.success-state {
  background: #ecfdf5;
  border: 1px solid #10b981;
  color: #065f46;
}

/* Celebratory moments */
@keyframes confetti {
  0% { opacity: 0; transform: translateY(-20px); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translateY(100vh); }
}

/* Delight in micro-interactions */
.like-button:active .heart {
  animation: heartBeat 0.3s ease;
}
```

---

## Learning & Memory

### Memory Types

1. **Sensory Memory** - Brief (<1 second)
2. **Short-term/Working Memory** - Limited (15-30 seconds)
3. **Long-term Memory** - Persistent storage

### Learning Principles
- **Repetition** - Reinforce through practice
- **Association** - Link to existing knowledge
- **Emotion** - Emotional events remembered better
- **Retrieval Practice** - Recall strengthens memory

### Design for Learning
```css
/* Consistent patterns aid learning */
.navigation {
  /* Same location on every page */
  position: fixed;
  top: 0;
}

/* Feedback reinforces correct actions */
.correct-answer {
  animation: pulse-green 0.5s;
}

/* Progress tracking */
.lesson-progress {
  /* Visual reminder of learning progress */
}
```

---

## Motivation

### Self-Determination Theory

1. **Autonomy** - Control over actions
2. **Competence** - Feeling effective
3. **Relatedness** - Connection to others

### Intrinsic vs Extrinsic Motivation
- Intrinsic: The activity itself is rewarding
- Extrinsic: External rewards (points, badges)

### Design for Motivation
```css
/* Autonomy - customization options */
.theme-selector {
  display: flex;
  gap: 12px;
}

/* Competence - skill progression */
.skill-tree {
  /* Visual progression showing mastery */
}

/* Relatedness - social features */
.team-activity {
  /* Show other users' activity */
}

/* Achievement indicators */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-radius: 9999px;
}
```

---

## Flow State

### Characteristics
- Complete absorption in activity
- Loss of self-consciousness
- Distorted sense of time
- Intrinsically rewarding

### Conditions for Flow
1. Clear goals
2. Immediate feedback
3. Challenge-skill balance

### Design for Flow
```css
/* Minimal distractions */
.focus-mode {
  /* Hide non-essential UI */
}

.focus-mode .sidebar,
.focus-mode .notifications {
  display: none;
}

/* Clear progress indication */
.writing-progress {
  position: fixed;
  top: 0;
  height: 3px;
  background: #3b82f6;
}

/* Immediate feedback */
.save-indicator {
  transition: opacity 0.2s;
}

.save-indicator.saving {
  opacity: 1;
}
```

---

## Summary: Psychology-Informed Design

### Checklist

**Cognitive Load**
- [ ] Essential information only
- [ ] Progressive disclosure for complexity
- [ ] Clear visual hierarchy

**Memory**
- [ ] Chunked information (5-9 items)
- [ ] External memory aids
- [ ] Recognition over recall

**Attention**
- [ ] Clear focus indicators
- [ ] Minimal distractions
- [ ] Guided visual flow

**Mental Models**
- [ ] Familiar patterns used
- [ ] Consistent interactions
- [ ] Clear system feedback

**Emotion**
- [ ] Positive first impression
- [ ] Satisfying interactions
- [ ] Meaningful completion states

**Motivation**
- [ ] User autonomy supported
- [ ] Progress visible
- [ ] Achievements recognized

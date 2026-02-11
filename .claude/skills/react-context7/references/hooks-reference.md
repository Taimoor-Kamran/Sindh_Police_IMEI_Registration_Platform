# React Hooks Reference

## useState

Declare state variable in a component.

```tsx
// Basic usage
const [count, setCount] = useState(0);

// With type inference
const [user, setUser] = useState<User | null>(null);

// Lazy initialization (expensive computation)
const [state, setState] = useState(() => {
  return computeExpensiveInitialValue();
});

// Functional updates (when new state depends on previous)
setCount(prev => prev + 1);

// Object state updates (always spread previous state)
setUser(prev => ({ ...prev, name: 'New Name' }));
```

### Best Practices
- Use separate `useState` calls for independent values
- Use `useReducer` for complex state logic
- Avoid putting derived values in state (compute during render)
- Use functional updates when new state depends on previous

## useEffect

Synchronize component with external system.

```tsx
// Basic effect
useEffect(() => {
  document.title = `Count: ${count}`;
}, [count]);

// Effect with cleanup
useEffect(() => {
  const subscription = subscribe(props.id);
  return () => {
    subscription.unsubscribe();
  };
}, [props.id]);

// Run once on mount
useEffect(() => {
  initializeAnalytics();
}, []);

// Async in effect (define async function inside)
useEffect(() => {
  async function fetchData() {
    const response = await fetch(url);
    const data = await response.json();
    setData(data);
  }
  fetchData();
}, [url]);
```

### Common Patterns

```tsx
// Fetch data
useEffect(() => {
  let cancelled = false;

  async function fetchData() {
    const response = await fetch(`/api/user/${userId}`);
    const data = await response.json();
    if (!cancelled) {
      setUser(data);
    }
  }

  fetchData();
  return () => { cancelled = true; };
}, [userId]);

// Event listener
useEffect(() => {
  function handleResize() {
    setWindowSize({ width: window.innerWidth, height: window.innerHeight });
  }

  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
}, []);

// Intersection Observer
useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => setIsVisible(entry.isIntersecting),
    { threshold: 0.1 }
  );

  if (ref.current) {
    observer.observe(ref.current);
  }

  return () => observer.disconnect();
}, []);
```

### Best Practices
- Each effect should do one thing
- Always include all referenced values in dependencies
- Use cleanup functions to prevent memory leaks
- Don't use effects for transforming data (do it during render)

## useContext

Read and subscribe to context from component.

```tsx
// Create context with type
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

// Custom hook for safe context consumption
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

// Provider component
function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = useCallback(() => {
    setTheme(t => t === 'light' ? 'dark' : 'light');
  }, []);

  const value = useMemo(() => ({ theme, toggleTheme }), [theme, toggleTheme]);

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// Usage in component
function ThemedButton() {
  const { theme, toggleTheme } = useTheme();
  return (
    <button className={theme} onClick={toggleTheme}>
      Toggle Theme
    </button>
  );
}
```

### Best Practices
- Create custom hooks for context consumption
- Memoize context value to prevent unnecessary re-renders
- Split contexts by update frequency
- Use context for truly global state only

## useReducer

Manage state with reducer function.

```tsx
// State and action types
interface State {
  count: number;
  step: number;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStep'; payload: number }
  | { type: 'reset' };

// Reducer function
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    case 'reset':
      return { count: 0, step: 1 };
    default:
      return state;
  }
}

// Usage
function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({ type: 'setStep', payload: Number(e.target.value) })}
      />
    </div>
  );
}
```

### When to Use
- Complex state logic with multiple sub-values
- Next state depends on previous state
- State updates are triggered from deep components (pass dispatch down)
- You want to optimize performance for components that trigger deep updates

## useCallback

Cache a function between re-renders.

```tsx
// Basic usage
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// With event handler
const handleSubmit = useCallback((e: FormEvent) => {
  e.preventDefault();
  submitForm(formData);
}, [formData]);

// Passing to memoized children
const MemoizedChild = memo(function Child({ onClick }: { onClick: () => void }) {
  return <button onClick={onClick}>Click me</button>;
});

function Parent() {
  const [count, setCount] = useState(0);

  // Without useCallback, new function every render, Child re-renders
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return (
    <>
      <MemoizedChild onClick={handleClick} />
      <button onClick={() => setCount(c => c + 1)}>Increment: {count}</button>
    </>
  );
}
```

### Best Practices
- Use with `memo()` children to prevent re-renders
- Use when passing callbacks to expensive child components
- Include all dependencies in the array
- Don't use everywhere - only when needed for optimization

## useMemo

Cache a calculation between re-renders.

```tsx
// Expensive calculation
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// Object creation for child props
const style = useMemo(() => ({
  backgroundColor: theme === 'dark' ? '#333' : '#fff',
  color: theme === 'dark' ? '#fff' : '#333',
}), [theme]);

// Derived state
const filteredUsers = useMemo(() => {
  return users.filter(user =>
    user.name.toLowerCase().includes(searchTerm.toLowerCase())
  );
}, [users, searchTerm]);

// Skip re-creating expensive component
const chart = useMemo(() => {
  return <ExpensiveChart data={data} />;
}, [data]);
```

### When to Use
- Expensive calculations (sorting, filtering large arrays)
- Creating objects/arrays passed to memoized children
- Values used as dependencies in other hooks
- Skip expensive re-renders

## useRef

Reference a value that doesn't need rendering.

```tsx
// DOM element reference
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </>
  );
}

// Mutable value that persists across renders
function Timer() {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const [count, setCount] = useState(0);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return <div>Count: {count}</div>;
}

// Previous value
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
}
```

### Common Use Cases
- Storing DOM element references
- Storing timeout/interval IDs
- Storing previous values
- Storing any mutable value that shouldn't trigger re-render

## useImperativeHandle

Customize ref handle exposed to parent.

```tsx
interface InputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

const FancyInput = forwardRef<InputHandle, { label: string }>(
  function FancyInput({ label }, ref) {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus() {
        inputRef.current?.focus();
      },
      clear() {
        if (inputRef.current) {
          inputRef.current.value = '';
        }
      },
      getValue() {
        return inputRef.current?.value ?? '';
      },
    }), []);

    return (
      <label>
        {label}
        <input ref={inputRef} type="text" />
      </label>
    );
  }
);

// Usage
function Form() {
  const inputRef = useRef<InputHandle>(null);

  const handleSubmit = () => {
    const value = inputRef.current?.getValue();
    console.log('Value:', value);
    inputRef.current?.clear();
  };

  return (
    <>
      <FancyInput ref={inputRef} label="Name" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

## useLayoutEffect

Fires before browser repaints screen. Use for DOM measurements.

```tsx
function Tooltip({ children, targetRef }: TooltipProps) {
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  useLayoutEffect(() => {
    if (targetRef.current && tooltipRef.current) {
      const targetRect = targetRef.current.getBoundingClientRect();
      const tooltipRect = tooltipRef.current.getBoundingClientRect();

      setPosition({
        top: targetRect.top - tooltipRect.height - 8,
        left: targetRect.left + (targetRect.width - tooltipRect.width) / 2,
      });
    }
  }, [targetRef]);

  return (
    <div
      ref={tooltipRef}
      style={{ position: 'fixed', top: position.top, left: position.left }}
    >
      {children}
    </div>
  );
}
```

### When to Use
- Measuring DOM elements before browser paints
- Synchronously updating DOM
- Avoiding visual flicker
- Note: Prefer `useEffect` for most cases

## useId

Generate unique IDs for accessibility attributes.

```tsx
function FormField({ label }: { label: string }) {
  const id = useId();

  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} type="text" />
    </div>
  );
}

// Multiple IDs
function PasswordField() {
  const id = useId();
  const passwordId = `${id}-password`;
  const confirmId = `${id}-confirm`;
  const errorId = `${id}-error`;

  return (
    <>
      <label htmlFor={passwordId}>Password</label>
      <input id={passwordId} type="password" aria-describedby={errorId} />

      <label htmlFor={confirmId}>Confirm</label>
      <input id={confirmId} type="password" />

      <span id={errorId} role="alert">Passwords must match</span>
    </>
  );
}
```

## useDeferredValue

Defer updating part of UI.

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(
    () => searchItems(deferredQuery),
    [deferredQuery]
  );

  return (
    <ul style={{ opacity: isStale ? 0.5 : 1 }}>
      {results.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
}
```

## useTransition

Update state without blocking UI.

```tsx
function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState('home');

  function selectTab(nextTab: string) {
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <>
      <TabButton onClick={() => selectTab('home')}>Home</TabButton>
      <TabButton onClick={() => selectTab('posts')}>Posts</TabButton>
      <TabButton onClick={() => selectTab('contact')}>Contact</TabButton>

      {isPending && <Spinner />}

      <TabPanel tab={tab} />
    </>
  );
}
```

## useSyncExternalStore

Subscribe to external store.

```tsx
// For subscribing to browser APIs or external state
function useOnlineStatus() {
  const isOnline = useSyncExternalStore(
    // subscribe
    (callback) => {
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    // getSnapshot (client)
    () => navigator.onLine,
    // getServerSnapshot (SSR)
    () => true
  );

  return isOnline;
}

// For external state management
const store = {
  state: { count: 0 },
  listeners: new Set<() => void>(),

  subscribe(listener: () => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  },

  getSnapshot() {
    return this.state;
  },

  increment() {
    this.state = { count: this.state.count + 1 };
    this.listeners.forEach(l => l());
  },
};

function useStore() {
  return useSyncExternalStore(
    store.subscribe.bind(store),
    store.getSnapshot.bind(store)
  );
}
```

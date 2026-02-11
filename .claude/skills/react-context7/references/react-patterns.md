# React Design Patterns

## Compound Components

Pattern for creating components that work together implicitly.

```tsx
// Parent manages shared state, children render pieces
interface TabsContextType {
  activeTab: string;
  setActiveTab: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [activeTab, setActiveTab] = useState(defaultTab);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: ReactNode }) {
  return <div role="tablist">{children}</div>;
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  return (
    <button
      role="tab"
      aria-selected={context.activeTab === id}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  if (context.activeTab !== id) return null;
  return <div role="tabpanel">{children}</div>;
}

// Attach sub-components
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage
<Tabs defaultTab="tab1">
  <Tabs.List>
    <Tabs.Tab id="tab1">First</Tabs.Tab>
    <Tabs.Tab id="tab2">Second</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel id="tab1">First content</Tabs.Panel>
  <Tabs.Panel id="tab2">Second content</Tabs.Panel>
</Tabs>
```

## Render Props

Pattern for sharing code between components using a prop whose value is a function.

```tsx
interface MousePosition {
  x: number;
  y: number;
}

interface MouseTrackerProps {
  render: (position: MousePosition) => ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return <>{render(position)}</>;
}

// Usage
<MouseTracker
  render={({ x, y }) => (
    <div>Mouse position: {x}, {y}</div>
  )}
/>

// Alternative: children as function
interface MouseTrackerChildrenProps {
  children: (position: MousePosition) => ReactNode;
}

function MouseTrackerAlt({ children }: MouseTrackerChildrenProps) {
  const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });
  // ... same logic
  return <>{children(position)}</>;
}
```

## Higher-Order Components (HOC)

Pattern for reusing component logic by wrapping components.

```tsx
interface WithLoadingProps {
  isLoading: boolean;
}

function withLoading<P extends object>(
  WrappedComponent: ComponentType<P>
): ComponentType<P & WithLoadingProps> {
  return function WithLoadingComponent({ isLoading, ...props }: P & WithLoadingProps) {
    if (isLoading) {
      return <div className="loading-spinner">Loading...</div>;
    }
    return <WrappedComponent {...(props as P)} />;
  };
}

// Usage
interface UserListProps {
  users: User[];
}

function UserList({ users }: UserListProps) {
  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}

const UserListWithLoading = withLoading(UserList);

// In parent
<UserListWithLoading isLoading={loading} users={users} />
```

## Custom Hooks

Pattern for extracting component logic into reusable functions.

```tsx
// useLocalStorage - Persist state to localStorage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
}

// useFetch - Data fetching with loading and error states
interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

function useFetch<T>(url: string): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const json = await response.json();
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// useDebounce - Debounce a value
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

## Controlled Components

Pattern for form inputs where React controls the value.

```tsx
interface FormData {
  email: string;
  password: string;
}

function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Partial<FormData>>({});

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user types
    if (errors[name as keyof FormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const validate = (): boolean => {
    const newErrors: Partial<FormData> = {};
    if (!formData.email.includes('@')) {
      newErrors.email = 'Invalid email';
    }
    if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="email"
        type="email"
        value={formData.email}
        onChange={handleChange}
        aria-invalid={!!errors.email}
      />
      {errors.email && <span className="error">{errors.email}</span>}

      <input
        name="password"
        type="password"
        value={formData.password}
        onChange={handleChange}
        aria-invalid={!!errors.password}
      />
      {errors.password && <span className="error">{errors.password}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

## Container-Presentational

Pattern separating data/logic from UI rendering.

```tsx
// Container: handles data fetching and state
function UserListContainer() {
  const { data: users, loading, error } = useFetch<User[]>('/api/users');
  const [selectedId, setSelectedId] = useState<string | null>(null);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!users) return null;

  return (
    <UserListView
      users={users}
      selectedId={selectedId}
      onSelect={setSelectedId}
    />
  );
}

// Presentational: pure rendering, no side effects
interface UserListViewProps {
  users: User[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

function UserListView({ users, selectedId, onSelect }: UserListViewProps) {
  return (
    <ul className="user-list">
      {users.map(user => (
        <li
          key={user.id}
          className={user.id === selectedId ? 'selected' : ''}
          onClick={() => onSelect(user.id)}
        >
          <Avatar src={user.avatar} />
          <span>{user.name}</span>
        </li>
      ))}
    </ul>
  );
}
```

## State Reducer Pattern

Pattern giving users full control over state changes.

```tsx
type ToggleState = { on: boolean };
type ToggleAction =
  | { type: 'toggle' }
  | { type: 'on' }
  | { type: 'off' };

function toggleReducer(state: ToggleState, action: ToggleAction): ToggleState {
  switch (action.type) {
    case 'toggle': return { on: !state.on };
    case 'on': return { on: true };
    case 'off': return { on: false };
    default: return state;
  }
}

interface UseToggleOptions {
  reducer?: (state: ToggleState, action: ToggleAction) => ToggleState;
}

function useToggle({ reducer = toggleReducer }: UseToggleOptions = {}) {
  const [{ on }, dispatch] = useReducer(reducer, { on: false });

  const toggle = () => dispatch({ type: 'toggle' });
  const setOn = () => dispatch({ type: 'on' });
  const setOff = () => dispatch({ type: 'off' });

  return { on, toggle, setOn, setOff };
}

// Usage: custom reducer to limit toggles
function limitedToggleReducer(state: ToggleState, action: ToggleAction): ToggleState {
  if (action.type === 'toggle' && clickCount >= maxClicks) {
    return state; // Prevent toggle
  }
  return toggleReducer(state, action);
}

const { on, toggle } = useToggle({ reducer: limitedToggleReducer });
```

## Prop Getters

Pattern providing props objects for consumers to spread.

```tsx
interface UseSelectableOptions<T> {
  items: T[];
  initialSelected?: T[];
  getId: (item: T) => string;
}

function useSelectable<T>({ items, initialSelected = [], getId }: UseSelectableOptions<T>) {
  const [selected, setSelected] = useState<Set<string>>(
    new Set(initialSelected.map(getId))
  );

  const isSelected = (item: T) => selected.has(getId(item));

  const toggle = (item: T) => {
    const id = getId(item);
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  // Prop getter - returns props to spread on item elements
  const getItemProps = (item: T) => ({
    'aria-selected': isSelected(item),
    onClick: () => toggle(item),
    role: 'option',
  });

  // Prop getter for container
  const getContainerProps = () => ({
    role: 'listbox',
    'aria-multiselectable': true,
  });

  return {
    selected: items.filter(isSelected),
    isSelected,
    toggle,
    getItemProps,
    getContainerProps,
  };
}

// Usage
function SelectableList({ items }: { items: Item[] }) {
  const { getContainerProps, getItemProps, selected } = useSelectable({
    items,
    getId: item => item.id,
  });

  return (
    <ul {...getContainerProps()}>
      {items.map(item => (
        <li key={item.id} {...getItemProps(item)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

## Error Boundary

Pattern for catching and handling errors in component trees.

```tsx
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback: ReactNode | ((error: Error, reset: () => void) => ReactNode);
}

interface ErrorBoundaryState {
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Send to error tracking service
  }

  reset = () => {
    this.setState({ error: null });
  };

  render() {
    const { error } = this.state;
    const { children, fallback } = this.props;

    if (error) {
      if (typeof fallback === 'function') {
        return fallback(error, this.reset);
      }
      return fallback;
    }

    return children;
  }
}

// Usage
<ErrorBoundary
  fallback={(error, reset) => (
    <div>
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={reset}>Try again</button>
    </div>
  )}
>
  <MyComponent />
</ErrorBoundary>
```

## Composition over Inheritance

Pattern preferring component composition for code reuse.

```tsx
// Instead of inheritance, compose with props
interface DialogProps {
  title: string;
  children: ReactNode;
  footer?: ReactNode;
  onClose: () => void;
}

function Dialog({ title, children, footer, onClose }: DialogProps) {
  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog" onClick={e => e.stopPropagation()}>
        <header className="dialog-header">
          <h2>{title}</h2>
          <button onClick={onClose} aria-label="Close">&times;</button>
        </header>
        <main className="dialog-body">{children}</main>
        {footer && <footer className="dialog-footer">{footer}</footer>}
      </div>
    </div>
  );
}

// Specialized dialogs through composition
function ConfirmDialog({
  message,
  onConfirm,
  onCancel
}: {
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  return (
    <Dialog
      title="Confirm"
      onClose={onCancel}
      footer={
        <>
          <button onClick={onCancel}>Cancel</button>
          <button onClick={onConfirm}>Confirm</button>
        </>
      }
    >
      <p>{message}</p>
    </Dialog>
  );
}
```

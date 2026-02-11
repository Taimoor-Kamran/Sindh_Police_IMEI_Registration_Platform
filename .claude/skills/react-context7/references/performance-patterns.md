# React Performance Patterns

## React.memo

Prevent re-renders when props haven't changed.

```tsx
// Basic usage
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});

// Custom comparison function
const UserCard = memo(
  function UserCard({ user }: { user: User }) {
    return (
      <div className="card">
        <img src={user.avatar} alt={user.name} />
        <h3>{user.name}</h3>
        <p>{user.email}</p>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Only re-render if user.id changes
    return prevProps.user.id === nextProps.user.id;
  }
);

// With children (children are always new reference)
const Panel = memo(function Panel({
  title,
  children
}: {
  title: string;
  children: ReactNode
}) {
  return (
    <section>
      <h2>{title}</h2>
      {children}
    </section>
  );
});

// Solution: move children creation inside or use useMemo
function App() {
  const content = useMemo(() => <ExpensiveContent />, []);
  return <Panel title="Dashboard">{content}</Panel>;
}
```

### When to Use
- Pure functional components with expensive rendering
- Components that re-render often with same props
- List item components
- Components receiving primitive props

### When NOT to Use
- Components that almost always receive different props
- Components that are already fast to render
- Components using context (they'll re-render anyway when context changes)

## useMemo Optimization

Cache expensive calculations.

```tsx
// Filtering and sorting
function UserList({ users, filter, sortBy }: UserListProps) {
  const processedUsers = useMemo(() => {
    const filtered = users.filter(user =>
      user.name.toLowerCase().includes(filter.toLowerCase())
    );

    return filtered.sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'date') return a.createdAt - b.createdAt;
      return 0;
    });
  }, [users, filter, sortBy]);

  return (
    <ul>
      {processedUsers.map(user => (
        <UserItem key={user.id} user={user} />
      ))}
    </ul>
  );
}

// Creating stable object references
function Component({ theme, size }: Props) {
  // Without useMemo: new object every render
  // const style = { color: theme.primary, fontSize: size };

  // With useMemo: stable reference
  const style = useMemo(() => ({
    color: theme.primary,
    fontSize: size,
  }), [theme.primary, size]);

  return <MemoizedChild style={style} />;
}

// Expensive computation
function DataVisualization({ data }: { data: DataPoint[] }) {
  const statistics = useMemo(() => {
    const sum = data.reduce((acc, point) => acc + point.value, 0);
    const mean = sum / data.length;
    const variance = data.reduce(
      (acc, point) => acc + Math.pow(point.value - mean, 2),
      0
    ) / data.length;
    const stdDev = Math.sqrt(variance);

    return { sum, mean, variance, stdDev };
  }, [data]);

  return <StatisticsDisplay stats={statistics} />;
}
```

## useCallback Optimization

Cache functions for memoized children.

```tsx
// Passing callbacks to memo children
const MemoizedButton = memo(function Button({
  onClick,
  children
}: {
  onClick: () => void;
  children: ReactNode
}) {
  console.log('Button rendered');
  return <button onClick={onClick}>{children}</button>;
});

function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  // These callbacks are stable - Button won't re-render when name/email change
  const handleSubmit = useCallback(() => {
    submitForm({ name, email });
  }, [name, email]);

  const handleReset = useCallback(() => {
    setName('');
    setEmail('');
  }, []);

  return (
    <form>
      <input value={name} onChange={e => setName(e.target.value)} />
      <input value={email} onChange={e => setEmail(e.target.value)} />
      <MemoizedButton onClick={handleSubmit}>Submit</MemoizedButton>
      <MemoizedButton onClick={handleReset}>Reset</MemoizedButton>
    </form>
  );
}

// Event handlers with parameters
function TodoList({ todos, onToggle }: TodoListProps) {
  // Create stable callback factory
  const createToggleHandler = useCallback(
    (id: string) => () => onToggle(id),
    [onToggle]
  );

  return (
    <ul>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={createToggleHandler(todo.id)}
        />
      ))}
    </ul>
  );
}
```

## Virtualization

Render only visible items in long lists.

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // estimated row height
    overscan: 5, // render 5 extra items above/below viewport
  });

  return (
    <div
      ref={parentRef}
      style={{ height: '400px', overflow: 'auto' }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Code Splitting with lazy

Load components on demand.

```tsx
import { lazy, Suspense } from 'react';

// Lazy load heavy components
const Dashboard = lazy(() => import('./Dashboard'));
const Analytics = lazy(() => import('./Analytics'));
const Settings = lazy(() => import('./Settings'));

function App() {
  const [page, setPage] = useState('dashboard');

  return (
    <div>
      <nav>
        <button onClick={() => setPage('dashboard')}>Dashboard</button>
        <button onClick={() => setPage('analytics')}>Analytics</button>
        <button onClick={() => setPage('settings')}>Settings</button>
      </nav>

      <Suspense fallback={<LoadingSpinner />}>
        {page === 'dashboard' && <Dashboard />}
        {page === 'analytics' && <Analytics />}
        {page === 'settings' && <Settings />}
      </Suspense>
    </div>
  );
}

// Preload on hover for faster navigation
function NavButton({ page, children }: NavButtonProps) {
  const preload = () => {
    if (page === 'analytics') {
      import('./Analytics');
    }
  };

  return (
    <button
      onMouseEnter={preload}
      onFocus={preload}
      onClick={() => setPage(page)}
    >
      {children}
    </button>
  );
}

// Named exports with lazy
const MyComponent = lazy(() =>
  import('./MyModule').then(module => ({ default: module.MyComponent }))
);
```

## Avoiding Unnecessary Re-renders

### State Colocation

Move state closer to where it's used.

```tsx
// Bad: state too high, causes entire form to re-render
function Form() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [bio, setBio] = useState('');

  return (
    <form>
      <NameInput value={name} onChange={setName} />
      <EmailInput value={email} onChange={setEmail} />
      <BioInput value={bio} onChange={setBio} /> {/* expensive */}
    </form>
  );
}

// Good: colocate state in child components
function Form() {
  return (
    <form>
      <NameField />
      <EmailField />
      <BioField /> {/* has its own state */}
    </form>
  );
}

function BioField() {
  const [bio, setBio] = useState('');
  return <BioInput value={bio} onChange={setBio} />;
}
```

### Component Splitting

Extract expensive parts.

```tsx
// Bad: ExpensiveChart re-renders when count changes
function Dashboard() {
  const [count, setCount] = useState(0);
  const data = useData();

  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>
        Count: {count}
      </button>
      <ExpensiveChart data={data} />
    </div>
  );
}

// Good: Counter is isolated
function Dashboard() {
  const data = useData();

  return (
    <div>
      <Counter />
      <ExpensiveChart data={data} />
    </div>
  );
}

function Counter() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

### Children as Props Pattern

Pass children to avoid re-renders.

```tsx
// Bad: SlowComponent re-renders when scroll position changes
function ScrollContainer() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div style={{ transform: `translateY(${scrollY * 0.5}px)` }}>
      <SlowComponent />
    </div>
  );
}

// Good: SlowComponent passed as children, doesn't re-render
function ScrollContainer({ children }: { children: ReactNode }) {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div style={{ transform: `translateY(${scrollY * 0.5}px)` }}>
      {children}
    </div>
  );
}

// Usage
<ScrollContainer>
  <SlowComponent />
</ScrollContainer>
```

## Transitions for Non-Urgent Updates

Keep UI responsive during expensive updates.

```tsx
function SearchPage() {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    // Urgent: update input immediately
    const value = e.target.value;

    // Non-urgent: wrap in transition
    startTransition(() => {
      setQuery(value);
    });
  };

  return (
    <div>
      <input onChange={handleChange} />
      {isPending ? (
        <div className="loading-overlay">Updating...</div>
      ) : null}
      <SearchResults query={query} />
    </div>
  );
}
```

## Deferred Values

Show stale content while fresh content loads.

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  // Use deferred value for expensive computation
  const results = useMemo(
    () => filterAndSortResults(allResults, deferredQuery),
    [deferredQuery]
  );

  return (
    <div style={{ opacity: isStale ? 0.7 : 1 }}>
      <ul>
        {results.map(result => (
          <ResultItem key={result.id} result={result} />
        ))}
      </ul>
    </div>
  );
}
```

## Profiling Performance

Use React DevTools Profiler.

```tsx
// Wrap sections you want to profile
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log({
    id,
    phase,
    actualDuration,
    baseDuration,
  });
}

function App() {
  return (
    <Profiler id="Navigation" onRender={onRenderCallback}>
      <Navigation />
    </Profiler>
  );
}
```

## Performance Checklist

1. **Identify slow renders** with React DevTools Profiler
2. **Memoize components** that receive same props often (`memo`)
3. **Memoize expensive calculations** (`useMemo`)
4. **Stabilize callbacks** passed to memoized children (`useCallback`)
5. **Virtualize long lists** (react-virtual, react-window)
6. **Code split** large components (`lazy` + `Suspense`)
7. **Colocate state** near where it's used
8. **Use transitions** for non-urgent updates
9. **Avoid new objects/arrays** in render (create outside or memoize)
10. **Split context** by update frequency

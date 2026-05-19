import './styles.css'

const users = [
  { name: 'Avery Admin', email: 'avery@example.com', role: 'Admin' },
  { name: 'Priya PM', email: 'priya@example.com', role: 'Project Manager' },
]

const customers = [
  { name: 'Northwind Health', priority: 'High', status: 'Active' },
  { name: 'Contoso Care', priority: 'Medium', status: 'Active' },
]

const projects = [
  { name: 'Portal Stabilization', customer: 'Northwind Health', status: 'Active' },
  { name: 'Mobile Rollout', customer: 'Contoso Care', status: 'Active' },
]

const ownershipRows = [
  {
    project: 'Portal Stabilization',
    vp: 'Morgan VP',
    director: 'Devon Director',
    pm: 'Priya PM',
    dl: 'Drew DL',
  },
]

export function App() {
  return (
    <main className="admin-shell">
      <header className="page-header">
        <p>Customer Health Projection Agent</p>
        <h1>Admin Configuration</h1>
      </header>

      <section className="role-strip" aria-label="Role-aware UI foundation">
        <div>
          <span className="eyebrow">Active role</span>
          <strong>Admin</strong>
        </div>
        <div>
          <span className="eyebrow">Allowed actions</span>
          <strong>Create and edit configuration</strong>
        </div>
        <div>
          <span className="eyebrow">View-only roles</span>
          <strong>VP, Project Director</strong>
        </div>
      </section>

      <div className="admin-grid">
        <section className="panel" aria-labelledby="users-heading">
          <div className="section-heading">
            <h2 id="users-heading">Users</h2>
            <button type="button">Add User</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.email}>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel" aria-labelledby="customers-heading">
          <div className="section-heading">
            <h2 id="customers-heading">Customers</h2>
            <button type="button">Add Customer</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Priority</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.name}>
                  <td>{customer.name}</td>
                  <td>{customer.priority}</td>
                  <td>{customer.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel" aria-labelledby="projects-heading">
          <div className="section-heading">
            <h2 id="projects-heading">Projects</h2>
            <button type="button">Add Project</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Customer</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.name}>
                  <td>{project.name}</td>
                  <td>{project.customer}</td>
                  <td>{project.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="panel ownership-panel" aria-labelledby="ownership-heading">
          <div className="section-heading">
            <h2 id="ownership-heading">Project Ownership</h2>
            <button type="button">Assign Owners</button>
          </div>
          <table>
            <thead>
              <tr>
                <th>Project</th>
                <th>VP</th>
                <th>Project Director</th>
                <th>PM</th>
                <th>DL</th>
              </tr>
            </thead>
            <tbody>
              {ownershipRows.map((row) => (
                <tr key={row.project}>
                  <td>{row.project}</td>
                  <td>{row.vp}</td>
                  <td>{row.director}</td>
                  <td>{row.pm}</td>
                  <td>{row.dl}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </main>
  )
}

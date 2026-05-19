import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { App } from './App'

describe('App', () => {
  it('renders the Admin Configuration shell', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', {
        name: /admin configuration/i,
      }),
    ).toBeInTheDocument()
  })

  it('renders Phase 01 admin sections', () => {
    render(<App />)

    expect(screen.getByRole('heading', { name: /users/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /customers/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /projects/i })).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: /project ownership/i }),
    ).toBeInTheDocument()
  })

  it('renders role-aware UI foundations', () => {
    render(<App />)

    expect(
      screen.getByRole('region', { name: /role-aware ui foundation/i }),
    ).toHaveTextContent(/admin/i)
    expect(screen.getByText(/create and edit configuration/i)).toBeInTheDocument()
    expect(screen.getByText(/vp, project director/i)).toBeInTheDocument()
  })

  it('renders Phase 01 configuration action buttons', () => {
    render(<App />)

    expect(screen.getByRole('button', { name: /add user/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /add customer/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /add project/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /assign owners/i })).toBeInTheDocument()
  })
})

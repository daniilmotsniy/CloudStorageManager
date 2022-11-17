import React from 'react'
import { render, screen } from '@testing-library/react'
import LoginPage from './page/LoginPage'

test('renders login page', () => {
  render(<LoginPage />)
  const linkElement1 = screen.getByText(/Username/i)
  const linkElement2 = screen.getByText(/Password/i)
  expect(linkElement1).toBeInTheDocument()
  expect(linkElement2).toBeInTheDocument()
})

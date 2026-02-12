import { render, screen } from '@testing-library/react';
import App from './App';

test('renders knowledge copilot heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/knowledge copilot/i);
  expect(headingElement).toBeInTheDocument();
});

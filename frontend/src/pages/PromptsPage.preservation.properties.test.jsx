import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import fc from 'fast-check';
import { readFileSync } from 'fs';
import { join } from 'path';
import CollectionsPage from './CollectionsPage';
import Sidebar from '../components/layout/Sidebar';
import Button from '../components/shared/Button';
import { ThemeProvider } from '../contexts/ThemeContext';

/**
 * Preservation Property Tests
 *
 * These tests verify that components already using correct CSS variables
 * remain unchanged after the bugfix. They should PASS on unfixed code.
 *
 * **Validates: Requirements 3.1, 3.2, 3.3**
 *
 * Strategy: Since we're in a test environment where CSS isn't fully computed,
 * we verify preservation by checking the CSS source files directly to ensure
 * they use the correct CSS variables and maintain their structure.
 *
 * Components being preserved:
 * 1. CollectionsPage header text styling (already uses var(--color-text-primary))
 * 2. Sidebar navigation styling (already uses var(--color-text-primary))
 * 3. Button layout properties (padding, border-radius, transitions)
 */

describe('PromptsPage Header Visibility - Preservation Tests', () => {
  it('Property 2: Preservation - CollectionsPage header uses correct CSS variable', async () => {
    /**
     * **Validates: Requirements 3.1, 3.2**
     *
     * CollectionsPage already uses var(--color-text-primary) correctly.
     * This test verifies the CSS file maintains this correct usage.
     *
     * EXPECTED OUTCOME: Test PASSES on unfixed code (baseline behavior)
     */

    await fc.assert(
      fc.asyncProperty(
        fc.constant(true),
        async () => {
          // Read the CollectionsPage CSS file
          const cssPath = join(process.cwd(), 'src/pages/CollectionsPage.module.css');
          const cssContent = readFileSync(cssPath, 'utf-8');

          // ASSERTION 1: CollectionsPage.module.css should use var(--color-text-primary)
          // This is the correct CSS variable for theme-aware text color
          expect(cssContent).toContain('var(--color-text-primary)');

          // ASSERTION 2: It should NOT use hardcoded colors like #333
          // The header h1 rule should use the CSS variable
          const headerH1Match = cssContent.match(/\.header\s+h1\s*\{[^}]*\}/s);
          expect(headerH1Match).toBeTruthy();
          expect(headerH1Match[0]).toContain('var(--color-text-primary)');

          // ASSERTION 3: Verify the component renders without errors
          const { container } = render(
            <BrowserRouter>
              <ThemeProvider>
                <CollectionsPage />
              </ThemeProvider>
            </BrowserRouter>
          );

          const header = container.querySelector('h1');
          expect(header).toBeTruthy();
          expect(header.textContent).toBe('Collections');

          return true;
        }
      ),
      { numRuns: 5 }
    );
  });

  it('Property 2: Preservation - Sidebar navigation uses correct CSS variable', async () => {
    /**
     * **Validates: Requirements 3.2, 3.3**
     *
     * Sidebar already uses var(--color-text-primary) for navigation links.
     * This test verifies the CSS file maintains this correct usage.
     *
     * EXPECTED OUTCOME: Test PASSES on unfixed code (baseline behavior)
     */

    await fc.assert(
      fc.asyncProperty(
        fc.constant(true),
        async () => {
          // Read the Sidebar CSS file
          const cssPath = join(process.cwd(), 'src/components/layout/Sidebar.module.css');
          const cssContent = readFileSync(cssPath, 'utf-8');

          // ASSERTION 1: Sidebar.module.css should use var(--color-text-primary)
          expect(cssContent).toContain('var(--color-text-primary)');

          // ASSERTION 2: The navLink rule should use the CSS variable
          const navLinkMatch = cssContent.match(/\.navLink\s*\{[^}]*\}/s);
          expect(navLinkMatch).toBeTruthy();
          expect(navLinkMatch[0]).toContain('var(--color-text-primary)');

          // ASSERTION 3: Verify the component renders without errors
          const { container } = render(
            <BrowserRouter>
              <ThemeProvider>
                <Sidebar isOpen={true} onClose={() => {}} />
              </ThemeProvider>
            </BrowserRouter>
          );

          const navLinks = container.querySelectorAll('a');
          expect(navLinks.length).toBeGreaterThan(0);

          return true;
        }
      ),
      { numRuns: 5 }
    );
  });

  it('Property 2: Preservation - Button layout properties defined in CSS', async () => {
    /**
     * **Validates: Requirements 3.3**
     *
     * Button layout properties (padding, border-radius, transitions) should
     * remain unchanged. Only the background-color CSS variable names are being fixed.
     *
     * EXPECTED OUTCOME: Test PASSES on unfixed code (baseline behavior)
     */

    await fc.assert(
      fc.asyncProperty(
        fc.constant(true),
        async () => {
          // Read the Button CSS file
          const cssPath = join(process.cwd(), 'src/components/shared/Button.module.css');
          const cssContent = readFileSync(cssPath, 'utf-8');

          // ASSERTION 1: Button CSS should contain layout properties
          expect(cssContent).toContain('padding:');
          expect(cssContent).toContain('border-radius:');
          expect(cssContent).toContain('transition:');

          // ASSERTION 2: Button base class should have these properties
          const buttonBaseMatch = cssContent.match(/\.button\s*\{[^}]*\}/s);
          expect(buttonBaseMatch).toBeTruthy();
          expect(buttonBaseMatch[0]).toContain('padding:');
          expect(buttonBaseMatch[0]).toContain('border-radius:');
          expect(buttonBaseMatch[0]).toContain('transition:');
          expect(buttonBaseMatch[0]).toContain('font-size:');

          // ASSERTION 3: Verify buttons render with correct structure
          const { container: primaryContainer } = render(
            <BrowserRouter>
              <ThemeProvider>
                <Button variant="primary">Primary</Button>
              </ThemeProvider>
            </BrowserRouter>
          );

          const primaryButton = primaryContainer.querySelector('button');
          expect(primaryButton).toBeTruthy();
          expect(primaryButton.textContent).toBe('Primary');

          return true;
        }
      ),
      { numRuns: 5 }
    );
  });

  it('Property 2: Preservation - Button disabled state uses hardcoded color', async () => {
    /**
     * **Validates: Requirements 3.3**
     *
     * Disabled button state uses hardcoded #ccc which should remain unchanged.
     * This test verifies the CSS maintains this behavior.
     *
     * EXPECTED OUTCOME: Test PASSES on unfixed code (baseline behavior)
     */

    await fc.assert(
      fc.asyncProperty(
        fc.constantFrom('primary', 'secondary', 'danger'),
        async (variant) => {
          // Read the Button CSS file
          const cssPath = join(process.cwd(), 'src/components/shared/Button.module.css');
          const cssContent = readFileSync(cssPath, 'utf-8');

          // ASSERTION 1: Disabled/loading state should use hardcoded #ccc
          const disabledMatch = cssContent.match(/\.button:disabled[^}]*\}/s) ||
                               cssContent.match(/\.button\.loading[^}]*\}/s);
          expect(disabledMatch).toBeTruthy();
          expect(cssContent).toContain('#ccc');
          expect(cssContent).toContain('cursor: not-allowed');

          // ASSERTION 2: Verify disabled button renders correctly
          const { container } = render(
            <BrowserRouter>
              <ThemeProvider>
                <Button variant={variant} disabled={true}>Disabled</Button>
              </ThemeProvider>
            </BrowserRouter>
          );

          const button = container.querySelector('button');
          expect(button).toBeTruthy();
          expect(button.disabled).toBe(true);

          return true;
        }
      ),
      { numRuns: 15 } // Test all three button variants
    );
  });
});

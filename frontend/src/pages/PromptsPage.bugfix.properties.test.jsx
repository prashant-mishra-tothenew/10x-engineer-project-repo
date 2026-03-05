import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { join } from 'path';
import fc from 'fast-check';

/**
 * Bug Condition Exploration Test
 *
 * This test is designed to FAIL on unfixed code to confirm the bugs exist.
 * It validates the expected behavior that will be satisfied after the fix.
 *
 * Bugs being tested:
 * 1. PromptsPage header uses hardcoded color #333 instead of var(--color-text-primary)
 * 2. Buttons use non-existent CSS variables (--primary-color, --secondary-color, --danger-color)
 *    instead of correct variables (--color-primary, --color-secondary, --color-danger)
 *
 * NOTE: This test checks the CSS source code directly because jsdom doesn't fully support
 * CSS custom properties in computed styles.
 */

describe('PromptsPage Header Visibility - Bug Condition Exploration', () => {
  it('Property 1: Fault Condition - Theme-Aware Text and Button Styling', () => {
    /**
     * **Validates: Requirements 2.1, 2.2, 2.3**
     *
     * For any CSS rule where hardcoded colors or non-existent CSS variables are used
     * for text or button styling, the fixed CSS SHALL use the correct theme-aware
     * CSS variables from variables.css, ensuring proper visibility and styling in
     * both light and dark themes.
     *
     * CRITICAL: This test MUST FAIL on unfixed code - failure confirms the bug exists.
     *
     * Expected counterexamples on unfixed code:
     * - PromptsPage.module.css uses `color: #333` instead of `color: var(--color-text-primary)`
     * - Button.module.css uses `var(--primary-color)` instead of `var(--color-primary)`
     * - Button.module.css uses `var(--secondary-color)` instead of `var(--color-secondary)`
     * - Button.module.css uses `var(--danger-color)` instead of `var(--color-danger)`
     */

    fc.assert(
      fc.property(
        // Test both CSS files that need fixing
        fc.constantFrom(
          { file: 'PromptsPage.module.css', path: 'src/pages/PromptsPage.module.css' },
          { file: 'Button.module.css', path: 'src/components/shared/Button.module.css' }
        ),
        (cssFile) => {
          // Read the CSS file content
          const cssPath = join(process.cwd(), cssFile.path);
          const cssContent = readFileSync(cssPath, 'utf-8');

          if (cssFile.file === 'PromptsPage.module.css') {
            // ASSERTION 1: PromptsPage header should use var(--color-text-primary)
            // On unfixed code: will contain "color: #333"
            // On fixed code: will contain "color: var(--color-text-primary)"

            // Check that hardcoded #333 is NOT present in header h1 rule
            const hasHardcodedColor = /\.header\s+h1\s*\{[^}]*color:\s*#333/s.test(cssContent);
            expect(hasHardcodedColor).toBe(false);

            // Check that the correct CSS variable IS present
            const hasCorrectVariable = /\.header\s+h1\s*\{[^}]*color:\s*var\(--color-text-primary\)/s.test(cssContent);
            expect(hasCorrectVariable).toBe(true);

          } else if (cssFile.file === 'Button.module.css') {
            // ASSERTION 2: Button component should use correct CSS variable names
            // On unfixed code: will contain var(--primary-color), var(--secondary-color), var(--danger-color)
            // On fixed code: will contain var(--color-primary), var(--color-secondary), var(--color-danger)

            // Check that incorrect variable names are NOT present
            const hasWrongPrimary = /var\(--primary-color\)/.test(cssContent);
            const hasWrongSecondary = /var\(--secondary-color\)/.test(cssContent);
            const hasWrongDanger = /var\(--danger-color\)/.test(cssContent);

            expect(hasWrongPrimary).toBe(false);
            expect(hasWrongSecondary).toBe(false);
            expect(hasWrongDanger).toBe(false);

            // Check that correct variable names ARE present
            const hasCorrectPrimary = /\.button\.primary\s*\{[^}]*background-color:\s*var\(--color-primary\)/s.test(cssContent);
            const hasCorrectSecondary = /\.button\.secondary\s*\{[^}]*background-color:\s*var\(--color-secondary\)/s.test(cssContent);
            const hasCorrectDanger = /\.button\.danger\s*\{[^}]*background-color:\s*var\(--color-danger\)/s.test(cssContent);

            expect(hasCorrectPrimary).toBe(true);
            expect(hasCorrectSecondary).toBe(true);
            expect(hasCorrectDanger).toBe(true);
          }

          return true;
        }
      ),
      { numRuns: 10 } // Test multiple times for both CSS files
    );
  });
});

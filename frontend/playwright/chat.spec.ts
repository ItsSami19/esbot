import { test, expect } from '@playwright/test'

async function createSessionAndOpen(page: any, title: string) {
  await page.getByTestId('new-session-btn').first().click()

  const input = page
    .locator('input.new-session-input, textarea.new-session-input')
    .first()
  await expect(input).toBeVisible()
  await input.fill(title)

  await input.press('Enter')

  await expect(page.getByTestId('message-input')).toBeVisible({
    timeout: 10_000,
  })
}

test.describe('Session Management', () => {
  test('TC-E2E-01: health badge is visible on load', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByTestId('health-status')).toBeVisible()
  })

  test('TC-E2E-02: create a new session and see it in sidebar', async ({
    page,
  }) => {
    await page.goto('/')
    const title = `E2E-Session-${Date.now()}`
    await createSessionAndOpen(page, title)
    await expect(page.getByTestId('session-list')).toContainText(title)
  })
})

test.describe('Chat Flow', () => {
  test('TC-E2E-03: send a message and receive AI reply', async ({ page }) => {
    await page.goto('/')
    await createSessionAndOpen(page, `Chat-Test-${Date.now()}`)

    await page.getByTestId('message-input').fill('Hello, what is Python?')
    await page.getByTestId('send-message-btn').click()

    await expect(page.getByTestId('user-message').first()).toBeVisible()
    await expect(page.getByTestId('user-message').first()).toContainText(
      'Hello, what is Python?',
    )

    const aiMsg = page.getByTestId('assistant-message').first()
    await expect(aiMsg).toBeVisible({ timeout: 10_000 })
    const aiText = await aiMsg.textContent()
    expect(aiText).toBeTruthy()
    expect(aiText!.length).toBeGreaterThan(0)
  })

  test('TC-E2E-04: message list shows history after reload', async ({
    page,
  }) => {
    await page.goto('/')
    await createSessionAndOpen(page, `History-Test-${Date.now()}`)

    await page.getByTestId('message-input').fill('Test history message')
    await page.getByTestId('send-message-btn').click()

    await expect(page.getByTestId('assistant-message').first()).toBeVisible({
      timeout: 10_000,
    })

    const msgList = page.getByTestId('message-list')
    await expect(msgList.getByTestId('user-message')).toHaveCount(1)
    await expect(msgList.getByTestId('assistant-message')).toHaveCount(1)
  })
})

test.describe('Negative / Error Cases', () => {
  test('TC-E2E-05: send button disabled when input is empty', async ({
    page,
  }) => {
    await page.goto('/')
    await createSessionAndOpen(page, `Negative-Test-${Date.now()}`)

    await expect(page.getByTestId('message-input')).toBeVisible()
    await expect(page.getByTestId('send-message-btn')).toBeDisabled()
  })

  test('TC-E2E-06: delete a session removes it from list', async ({ page }) => {
    await page.goto('/')
    const title = `Delete-Me-${Date.now()}`
    await createSessionAndOpen(page, title)

    await expect(page.getByTestId('session-list')).toContainText(title)

    const sessionItem = page.locator('.session-item').filter({ hasText: title })
    await sessionItem.hover()
    await sessionItem.locator('.session-delete-btn').click()

    await expect(page.getByTestId('session-list')).not.toContainText(title)
  })
})

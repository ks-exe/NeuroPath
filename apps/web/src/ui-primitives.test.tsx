import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Button, Card, Field, Heading, MonoLabel, Section } from "@neuropath/ui";

describe("Field", () => {
  it("links the label to the input and has no error state by default", () => {
    render(<Field id="email" label="Email" />);
    const input = screen.getByLabelText("Email");
    expect(input).toHaveAttribute("id", "email");
    expect(input).not.toHaveAttribute("aria-invalid");
  });

  it("sets aria-invalid and aria-describedby when an error is given", () => {
    render(<Field id="email" label="Email" hint="Work address" error="Required" />);
    const input = screen.getByLabelText("Email");
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(input.getAttribute("aria-describedby")?.split(" ")).toEqual(["email-hint", "email-error"]);
    const alert = screen.getByRole("alert");
    expect(alert).toHaveAttribute("id", "email-error");
    expect(alert).toHaveTextContent("Required");
  });
});

describe("primitives", () => {
  it("render without gradient or blur classes", () => {
    const { container } = render(
      <Section>
        <Heading level={2}>Title</Heading>
        <MonoLabel>LABEL</MonoLabel>
        <Card>Body</Card>
        <Button>Go</Button>
      </Section>,
    );
    expect(screen.getByRole("button", { name: "Go" })).toHaveAttribute("type", "button");
    expect(container.innerHTML).not.toMatch(/bg-gradient-|backdrop-blur/);
  });
});

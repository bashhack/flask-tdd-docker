import React from "react";
import { render, cleanup } from "@testing-library/react";

import RegisterForm from "../RegisterForm";

afterEach(cleanup);

const props = {
  handleRegisterFormSubmit: () => {
    return true;
  }
};

it("renders", () => {
  const { asFragment } = render(<RegisterForm {...props} />);
  expect(asFragment()).toMatchSnapshot();
});

it("renders properly", () => {
  const { getByText } = render(<RegisterForm {...props} />);
  expect(getByText("Register")).toHaveClass("title");
});

it("renders with default props", () => {
  const { getByLabelText, getByText } = render(<RegisterForm {...props} />);

  const usernameInput = getByLabelText("Username");
  expect(usernameInput).toHaveAttribute("type", "text");
  expect(usernameInput).not.toHaveValue();

  const emailInput = getByLabelText("Email");
  expect(emailInput).toHaveAttribute("type", "email");
  expect(emailInput).not.toHaveValue();

  const passwordInput = getByLabelText("Password");
  expect(passwordInput).toHaveAttribute("type", "password");
  expect(passwordInput).not.toHaveValue();

  const inputSubmit = getByText("Submit");
  expect(inputSubmit).toHaveValue("Submit");
});

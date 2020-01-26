import React from "react";
import { render, cleanup } from "@testing-library/react";

import RegisterForm from "../RegisterForm";

afterEach(cleanup);

it("renders", () => {
  const { asFragment } = render(<RegisterForm />);
  expect(asFragment()).toMatchSnapshot();
});

it("renders properly", () => {
  const { getByText } = render(<RegisterForm />);
  expect(getByText("Register")).toHaveClass("title");
});

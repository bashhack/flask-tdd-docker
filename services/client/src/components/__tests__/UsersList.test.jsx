import React from 'react';
import { render, cleanup } from '@testing-library/react';

import UsersList from '../UsersList';

afterEach(cleanup);

const users = [
    {
        'email': 'testuser1@example.com',
        'id': 1,
        'username': 'testuser1'
    },
    {
        'email': 'testuser2@example.com',
        'id': 2,
        'username': 'testuser2'
    }
];

it('renders', () => {
    const { asFragment } = render(<UsersList users={users}/>);
    expect(asFragment()).toMatchSnapshot();
});

it('renders a username', () => {
    const { getByText } = render(<UsersList users={users}/>);
    expect(getByText('testuser1')).toHaveClass('username');
    expect(getByText('testuser2')).toHaveClass('username');
});
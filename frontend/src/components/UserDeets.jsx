import React, { useContext } from 'react'
import { UserContext } from '../App';

export default function UserDeets() {
    const {user, setUser} = useContext(UserContext)
    console.log(`user deets context user:${user}`);
return (
    <div>
      Welcome: {user}
    </div>
  );
}
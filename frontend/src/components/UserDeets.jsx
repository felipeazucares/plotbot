import React, { useContext } from 'react'
import { PlotbotContext } from '../App';

export default function UserDeets() {
    const {user, setUser} = useContext(PlotbotContext)
    console.log(`user deets context user:${user}`);
return (
    <div>
      Welcome: {user}
    </div>
  );
}
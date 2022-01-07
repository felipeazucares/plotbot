import React, { useContext } from 'react'
import { PlotbotContext } from '../App';

export default function UserDeets() {
    const user = useContext(PlotbotContext)
return (
    <div>
      Welcome: {user.name}
    </div>
  );
}
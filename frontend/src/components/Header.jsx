import React from "react";
import { Text, Heading } from '@chakra-ui/react'
const Header = () => {
  return (
    // <Flex
    //   as="nav"
    //   align="center"
    //   justify="space-between"
    //   wrap="wrap"
    //   padding="0.5rem"
    // >
    //   <Flex align="center" mr={5}>
    //     <Heading as="h1" size="lg">Building Interactive Fiction with PlotBot</Heading>
    //   </Flex>
    // </Flex>
    <span>
      <Heading fontSize='5xl'>PlotterBot</Heading>
      <Text fontSize='xs'>Interactive fiction powered by AiTextGen & Mongodb</Text>
    </span>
  );
};


export default Header;
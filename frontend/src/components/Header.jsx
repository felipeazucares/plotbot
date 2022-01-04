import React from "react";
import { Heading, Flex, Divider } from "@chakra-ui/react";

const Header = () => {
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="0.5rem"
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg">Building Interactive Fiction with PlotBot</Heading>
      </Flex>
    </Flex>
  );
};

export default Header;
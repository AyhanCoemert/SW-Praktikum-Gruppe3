import * as React from 'react';
import {Stack, Button} from '@mui/material';
import { Link } from 'react-router-dom';

//@author [Soumayyah Aboubakar](https://github.com/soumayyahaboubakar)

export default function Semester() {
  return (
    <Stack spacing={2} direction="columns">
      <Button variant="contained">WS19/20</Button>
      <Button variant="contained">SS20</Button>
      <Button variant="contained">WS20/21</Button>
      <Button variant="contained">SS21</Button>
      <Button variant="contained">WS21/22</Button>  
    </Stack>

    
     
  );
}
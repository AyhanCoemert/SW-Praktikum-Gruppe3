import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom';



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
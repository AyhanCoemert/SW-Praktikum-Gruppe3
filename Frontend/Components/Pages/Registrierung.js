import React, { Component } from 'react';
import { Button, Grid, Typography, withStyles } from '@material-ui/core';

  
class SignIn extends Component {

	handleSignInButtonClicked = () => {
		this.props.onSignIn();
	}
    
	render() {
	

		return (
			<div>
				<Typography  align='center'>Registriert dich </Typography>
				<Typography  align='center'>Gib deinen Daten ein</Typography>
				<Grid container direction="column"  justify="space-between" alignItems="center" spacing={2}>
					<Grid item>
						<Button variant='contained' color='primary' onClick={this.handleSignInButtonClicked}>
							Login
      			</Button>
                	</Grid> 
				</Grid>
			</div>
		);
	}
}



export default Registrierung

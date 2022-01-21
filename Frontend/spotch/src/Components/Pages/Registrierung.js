import React, {useRef} from 'react'
import {Form, Button, Card} from 'react-bootstrap'


export default function Registrierung() {
	const emailRef = useRef()
	const passwortRef = useRef()
	const passwortConfirmRef = useRef()

	return (
		<>
		<Card>
			<Card.Body>
				<h2 className="text-center mb-4">Anmelden</h2>
				<Form>
					
				<Form.Group id = "email">
					<Form.Label>Email</Form.Label>
					<Form.Control type="email" ref={emailRef} required />
				</Form.Group>

				<Form.Group id = "passwort">
					<Form.Label>Passwort</Form.Label>
					<Form.Control type="passwort" ref={passwortRef} required />
				</Form.Group>

				<Form.Group id = "passwort-confirm">
					<Form.Label>Passwort-Confirmation</Form.Label>
					<Form.Control type="passwort" ref={passwortConfirmRef} required />
				</Form.Group>

				<Button className="w-100" type="submit">Anmelden</Button>

				</Form>

			</Card.Body>
		</Card>	
		<div className="w-100 text-center mt-2">
		 Haben Sie bereits ein Konto? Loggen Sie sich ein
		</div>
		</>
	)
}





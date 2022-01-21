import React, {useRef, useState} from 'react'
import {Form, Button, Card, Alert} from 'react-bootstrap'
import { useAuth } from '../../contexts/AuthContext'


export default function Registrierung() {
	const emailRef = useRef()
	const passwortRef = useRef()
	const passwortConfirmRef = useRef()
	const { registrierung } = useAuth()
	const [error, setError] = useState('')
	const [loading, setLoading] = useState(false)

	async function handleSubmit(e){
		e.preventDefault()

		if (passwortRef.current.value !== passwortConfirmRef.current.value){
			return setError('Passwords does not match')

		}

		try{
			setError('')
			setLoading(true)
			await registrierung(emailRef.current.value, passwortRef.current.value)
		} catch{
			setError('Failed to create an Account')
		}
		
		setLoading(false)

		
	}



	return (
		<>
		<Card>
			<Card.Body>
				<h2 className="text-center mb-4">Anmelden</h2>
				{error && <Alert variant = "danger">{error}</Alert>}
				<Form onSubmit={handleSubmit}>
					
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

				<Button disabled = {loading} className="w-100" type="submit"> Anmelden
				</Button>

				</Form>

			</Card.Body>
		</Card>	
		<div className="w-100 text-center mt-2">
		 Haben Sie bereits ein Konto? Loggen Sie sich ein
		</div>
		</>
	)
}





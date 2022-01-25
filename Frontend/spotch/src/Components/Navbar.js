import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { auth, db } from "../firebase";
import { signOut } from "firebase/auth";
import { updateDoc, doc } from "firebase/firestore";
import { AuthContext } from "../context/auth";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const handleSignout = async () => {
    await updateDoc(doc(db, "users", auth.currentUser.uid), {
      isOnline: false,
    });
    await signOut(auth);
    navigate.replace("/login");
  };
  return (
    <nav>
      <h3>
        <Link to="/"></Link>
      </h3>
      <div>
        {user ? (
          <>
            <Link to="/">...</Link>
            <button className="btn" onClick={handleSignout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="">..</Link>
            <Link to="/"></Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
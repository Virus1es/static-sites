import nox

@nox.session
def build(session: nox.Session) -> None:
    """Generate experiment results and build the Nikola site."""
    session.install("-r", "requirements.txt")
    
    session.run("python", "scripts/analyze.py")
    session.run("nikola", "build")
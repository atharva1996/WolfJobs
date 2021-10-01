import unittest
import application


class BasicTestCase(unittest.TestCase):



    def test_dummy(self):
        self.app = application.app.test_client()
        ans =self.app.get('/dummy')
        self.assertEqual(ans.status_code,200)

    
    def test_about(self):
        self.app = application.app.test_client()
        ans =self.app.get('/about')
        self.assertEqual(ans.status_code,200)

    def test_home(self):
        self.app = application.app.test_client()
        ans =self.app.get('/home')
        self.assertEqual(ans.status_code,302)

    def test_login(self):
        self.app = application.app.test_client()
        ans =self.app.get('/login')
        self.assertEqual(ans.status_code,200)

    def test_register(self):
        self.app = application.app.test_client()
        ans =self.app.get('/register')
        self.assertEqual(ans.status_code,200)

    def test_logout(self):
        self.app = application.app.test_client()
        ans =self.app.get('/logout')
        self.assertEqual(ans.status_code,200)  

    def test_forgotpassword(self):
        self.app = application.app.test_client()
        ans =self.app.get('/forgotpassword')
        self.assertEqual(ans.status_code,200)  

    def test_posting(self):
        self.app = application.app.test_client()
        ans =self.app.get('/posting')
        self.assertEqual(ans.status_code,302)

    def test_applying(self):
        self.app = application.app.test_client()
        ans =self.app.get('/applying')
        self.assertEqual(ans.status_code,302)


    def test_deletejob(self):
        self.app = application.app.test_client()
        ans =self.app.get('/deleteJob')
        self.assertEqual(ans.status_code,302)

    def test_selectApplicant(self):
        self.app = application.app.test_client()
        ans =self.app.get('/selectApplicant')
        self.assertEqual(ans.status_code,302)
    
    def test_jobsApplied(self):
        with application.app.test_client() as client:
            with client.session_transaction() as session:
                session['login_type']='Manager'
        ans =self.app.get('/jobsApplied')
        self.assertEqual(ans.status_code,302)
        print(session)
        yield client

    def test_dashboard(self):
        with application.app.test_client() as client:
            with client.session_transaction() as session:
                session['login_type']='Manager'
        ans =self.app.get('/dashboard')
        self.assertEqual(ans.status_code,302)
        print(session)
        yield client

if __name__ == '__main__':
    unittest.main()

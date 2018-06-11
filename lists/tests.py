from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from lists.forms import TaskForm
from lists.models import Todo

class TaskTests(TestCase):
	""" TaskTest class to test all the function of Todo model and view"""
	print("setUpTestData: Run once to set up non-modified data for all class methods.")
	pass
	def setUp(self):
		self.user = User.objects.create_user(
			'test', 'test@gmail.com', 'test123'
			)
		self.tasklist = Todo(description='hello this is testing', creator=self.user)
		self.tasklist.save()
		self.client.login(username='test', password='test123')

	def tearDown(self):
		self.client.logout()
		self.user.delete()
		self.tasklist.delete()


	def test_get_index_page(self):
		"""test all the task list"""
		response = self.client.get(reverse('lists:alllist'))
		self.assertTemplateUsed(response, 'lists/task_list.html')


		""" test user dashboard """
	def test_user_profile_page(self):
		response = self.client.get(
            reverse('lists:profile'), {'description': 'test'})
		self.assertTemplateUsed(response, 'lists/profile.html')


		
	def test_get_update_task_view(self):
		"""test  task update by particular user """
		response = self.client.post(
            reverse(
                'lists:update', kwargs={'id': self.tasklist.id}))
		self.assertTemplateUsed(response, 'lists/update_task.html')
		self.assertIsInstance(response.context['form'], TaskForm)


		
	def test_get_redirect_when_delete_task_view(self):
		""" testing function for deleting task"""
		response = self.client.post(
            reverse(
                'lists:delete', kwargs={'tasklist_id': self.tasklist.id}))
		self.assertRedirects(response, reverse('lists:alllist'), fetch_redirect_response=False)

	def test_get_status_update_when_mark_view(self):
		"""status update when user mark a task and button will get automaticall disabled """
		response = self.client.post(
            reverse(
                'lists:status', kwargs={'id': self.tasklist.id}))
		self.assertRedirects(response, reverse('lists:alllist'), fetch_redirect_response=False)
		
     
		
     





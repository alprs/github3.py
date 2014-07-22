# -*- coding: utf-8 -*-
"""Integration tests for methods implemented on Organization."""
import pytest

import github3

from .helper import IntegrationHelper


class TestOrganization(IntegrationHelper):

    """Organization integration tests."""

    betamax_kwargs = {'match_requests_on': ['method', 'uri', 'json-body']}

    def test_add_member(self):
        """Test the ability to add a member to an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('add_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)
            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'
            assert o.add_member('esacteksab', team.id) is True

    def test_add_repository(self):
        """Test the ability to add a repository to an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('add_repository')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'

            assert o.add_repository('github3py/urllib3', team.id) is True

    def test_create_repository(self):
        """Test the ability to create a repository in an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('create_repository')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            r = o.create_repository('test-repository', description='hi')
            assert isinstance(r, github3.repos.Repository)
            assert r.delete() is True

    def test_conceal_member(self):
        """Test the ability to conceal a User's membership."""
        self.basic_login()
        cassette_name = self.cassette_name('conceal_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            # Get a public member of the organization
            public_member = next(o.public_members())
            assert isinstance(public_member, github3.users.User)

            # Conceal their membership
            assert o.conceal_member(public_member) is True
            # Re-publicize their membership
            assert o.publicize_member(public_member) is True

    def test_create_team(self):
        """Test the ability to create a new team."""
        self.basic_login()
        cassette_name = self.cassette_name('create_team')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            t = o.create_team('temp-team')
            assert isinstance(t, github3.orgs.Team)
            assert t.delete() is True

    def test_edit(self):
        """Test the ability to edit an organization."""
        self.basic_login()
        cassette_name = self.cassette_name('edit')
        with self.recorder.use_cassette(cassette_name, **self.betamax_kwargs):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            assert o.edit(location='Madison, WI') is True

    def test_is_member(self):
        """Test the ability to check if a User is a member of the org."""
        cassette_name = self.cassette_name('is_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            assert o.is_member('sigmavirus24') is True

    def test_is_public_member(self):
        """Test the ability to check if a User is a public member."""
        cassette_name = self.cassette_name('is_public_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            assert o.is_public_member('defunkt') is False

    def test_events(self):
        """Test the ability to retrieve an organization's event stream."""
        cassette_name = self.cassette_name('events')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for event in o.events():
                assert isinstance(event, github3.events.Event)

    def test_members(self):
        """Test the ability to retrieve an organization's members."""
        self.basic_login()
        cassette_name = self.cassette_name('members')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for member in o.members():
                assert isinstance(member, github3.users.User)

    def test_public_members(self):
        """Test the ability to retrieve an organization's public members."""
        self.basic_login()
        cassette_name = self.cassette_name('public_members')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for member in o.public_members():
                assert isinstance(member, github3.users.User)

    def test_repositories(self):
        """Test the ability to retrieve an organization's repositories."""
        cassette_name = self.cassette_name('repositories')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for repo in o.repositories():
                assert isinstance(repo, github3.repos.Repository)

    def test_teams(self):
        """Test the ability to retrieve an organization's teams."""
        self.basic_login()
        cassette_name = self.cassette_name('teams')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            for team in o.teams():
                assert isinstance(team, github3.orgs.Team)

    def test_publicize_member(self):
        """Test the ability to publicize a member of the organization."""
        self.basic_login()
        cassette_name = self.cassette_name('publicize_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            # Show that we cannot publicize someone other than the current
            # user
            with pytest.raises(github3.GitHubError):
                o.publicize_member('esacteksab')

            assert o.publicize_member('sigmavirus24') is True

    def test_remove_member(self):
        """Test the ability to remove a member of the organization."""
        self.basic_login()
        cassette_name = self.cassette_name('remove_member')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            # First find the team we want to use
            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'

            # First add the user
            assert o.add_member('gh3test', team.id) is True
            # Now remove them
            assert o.remove_member('gh3test') is True

    def test_remove_repository(self):
        """Test the ability to remove a repository from a team."""
        self.basic_login()
        cassette_name = self.cassette_name('remove_repository')
        with self.recorder.use_cassette(cassette_name):
            o = self.gh.organization('github3py')
            assert isinstance(o, github3.orgs.Organization)

            # First find the team we want to use
            for team in o.teams():
                if team.name == 'Do Not Delete':
                    break
            else:
                assert False, 'Could not find team'

            assert o.remove_repository('github3py/urllib3', team.id) is True

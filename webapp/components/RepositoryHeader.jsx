import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Link} from 'react-router';
import styled from 'styled-components';

import Header from '../components/Header';

const Nav = styled.div`
  display: inline-block;
  margin-left: 40px;
`;

const NavItem = styled(Link)`
  cursor: pointer;
  float: left;
  font-size: 15px;
  color: #333;
  margin-left: 10px;
  padding: 5px 10px;
  border: 3px solid #fff;
  border-radius: 4px;

  &:hover {
    color: #333;
  }

  &.active, .${props => props.activeClassName} {
    border-color: #7B6BE6;
    color: #7B6BE6;
  }
`;

NavItem.defaultProps = {
  activeClassName: 'active'
};

export default class RepositoryHeader extends Component {
  static contextTypes = {
    repo: PropTypes.object.isRequired
  };

  render() {
    let {repo} = this.context;
    let basePath = `/${repo.full_name}`;

    return (
      <Header>
        <RepoName>
          {repo.owner_name} / {repo.name}
        </RepoName>
        <Nav>
          <NavItem to={basePath} onlyActiveOnIndex={true}>
            Commits
          </NavItem>
          <NavItem to={`${basePath}/builds`}>Builds</NavItem>
          <NavItem to={`${basePath}/tests`}>Tests</NavItem>
          <NavItem to={`${basePath}/settings`}>Settings</NavItem>
        </Nav>
      </Header>
    );
  }
}

const RepoName = styled.h1`
  float: left;
  font-size: 24px;
  margin: 0;
  line-height: 36px;
  letter-spacing: -1px;
  text-transform: uppercase;
  font-weight: 500;
`;

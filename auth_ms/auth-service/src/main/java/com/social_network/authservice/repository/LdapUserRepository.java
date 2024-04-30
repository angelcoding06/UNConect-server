package com.social_network.authservice.repository;

import java.util.Optional;
import org.springframework.data.ldap.repository.LdapRepository;
import org.springframework.stereotype.Repository;
import com.social_network.authservice.entity.LdapUser;

@Repository
public interface LdapUserRepository extends LdapRepository<LdapUser> {
	Optional<LdapUser> findByEmail(String email);
}

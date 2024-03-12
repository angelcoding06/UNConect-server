package com.social_network.authservice.repository;

import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import com.social_network.authservice.entity.AuthUser;
import com.social_network.authservice.entity.Role;
import jakarta.transaction.Transactional;
import java.util.List;


@Repository
public interface AuthUserRepository extends JpaRepository<AuthUser, UUID> {
	Optional<AuthUser> findById(UUID id);

	Optional<AuthUser> findByEmail(String userName);

	List<AuthUser> findByRole(Role role);

	@Modifying
	@Transactional
	@Query(value = "UPDATE auth_user SET email = ?1, password = ?2, is_verified = ?3, role = ?4 WHERE id = ?5",
			nativeQuery = true)
	void updateById(String email, String password, boolean isVerified, Role role, UUID id);
}

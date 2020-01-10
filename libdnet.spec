%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Summary:	Simple portable interface to lowlevel networking routines
Name:		libdnet

Version:	1.12
Release:	11%{?dist}

License:	BSD
Group:		System Environment/Libraries
URL:		http://code.google.com/p/%{name}/

Source:		http://%{name}.googlecode.com/files/%{name}-%{version}.tgz
Patch0:		%{name}-shrext.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
libdnet provides a simplified, portable interface to several
low-level networking routines, including network address
manipulation, kernel arp(4) cache and route(4) table lookup and
manipulation, network firewalling (IP filter, ipfw, ipchains,
pf, ...), network interface lookup and manipulation, raw IP
packet and Ethernet frame, and data transmission.

%package devel
Summary:	Header files for libdnet library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
%{summary}.

%package progs
Summary:	Sample applications to use with libdnet
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}

%description progs
%{summary}.

%package python
Summary:	Python bindings for libdnet
Requires:	%{name} = %{version}-%{release}
BuildRequires:	python-devel

%description python
%{summary}.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%{__make} %{?_smp_mflags}

pushd python
%{__python} setup.py build
popd

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

pushd python
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README THANKS TODO
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so
%exclude %{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man3/*.3*

%files progs
%defattr(-,root,root,-)
%{_sbindir}/*
%{_mandir}/man8/*.8*

%files python
%{python_sitearch}/*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Oliver Falk <oliver@linux-kernel.at> - 1.12-10
- Add python bindings in -python subpackage (BZ#815524)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 12 2010 Oliver Falk <oliver@linux-kernel.at> - 1.12-6
- Disable build of static libs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.12-3
- Bump-n-build for GCC 4.3

* Tue Aug 21 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.12-2
- Rebuild for BuildID
- Changed license tag to be more conformant

* Thu Feb 15 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.12-1
- New upstream version
- New upstream web site (thanks JPO!)
- Patch for inconsistent shrext variable
- Minor edits for consistency

* Wed Jan 24 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.10-5
- Converted spec to UTF-8 to fix BZ#222794

* Wed Oct 04 2006 Patrick "Jima" Laughton <jima@beer.tclug.org> 1.10-4
- Bump-n-build
- Reverted to 1.10; 1.11 has some serious issues

* Tue Sep 19 2006 Patrick "Jima" Laughton <jima@beer.tclug.org>	- 1.10-3
- Bump for FC6 rebuild

* Thu Jul 14 2005 Oliver Falk <oliver@linux-kernel.at>		- 1.10-2
- Integrate Josщ's patch after reviewing the pkg.

* Fri Jul 08 2005 Oliver Falk <oliver@linux-kernel.at>		- 1.10-1
- Build for FE

#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A collection of Python wrappers to facilitate access to azure key vault.

There are several options to setup access for an application or process to Azure AD. 
One is to setup service principals. The link below gives a quick overview of how to setup
a service principal and give it access to a specific key vault
'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import absolute_import, division, print_function, unicode_literals

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from getpass import getpass
from ..pynomial_configuration import Configurations

class SPCredential(ClientSecretCredential):
    
    
    def __init__(self, client_id=None, tenant_id=None, client_secret=None):
        
        '''
        
        Parameters:
        
            tenant_id (str) – ID of the service principal’s tenant. Also called its ‘directory’ ID.
            client_id (str) – the service principal’s client ID
            client_secret (str) – one of the service principal’s client secrets

        Examples:

        .. code-block:: python
            
            import pynomial as pyn

            credential = pyn.SPCredential()

            >>> Client ID was retrieved from AZURE_CLIENT_ID environmental variable
            >>> Tenant ID was retrieved from AZURE_Tenant_ID environmental variable
            >>> Client secret was retrieved from AZURE_CLIENT_SECRET environmental variable
            
        '''
        
        # Retrieve client_id
        if client_id is None:
            
            if Configurations['Azure.SP.client_id'] is None:
                
                if os.getenv('AZURE_CLIENT_ID') is None:
                    
                    client_id = getpass('Client ID: ')
                    
                else:
                    print('Client ID was retrieved from AZURE_CLIENT_ID environmental variable')
                    client_id = os.getenv('AZURE_CLIENT_ID')
            else:
                client_id = Configurations['Azure.SP.client_id']
                
             
        if client_id is None:
            raise ValueError('Client ID needs to be provided')
        else:
            self.client_id = client_id
        
        
        # Retrieve tenant_id
        if tenant_id is None:
            
            if Configurations['Azure.SP.tenant_id'] is None:
                
                if os.getenv('AZURE_TENANT_ID') is None:
                    
                    tenant_id = getpass('Tenant ID: ')
                    
                else:
                    print('Tenant ID was retrieved from AZURE_Tenant_ID environmental variable')
                    tenant_id = os.getenv('AZURE_TENANT_ID')
            else:
                tenant_id = Configurations['Azure.SP.TENANT_ID']
                
        
        if tenant_id is None:
            raise ValueError('Tenant ID needs to be provided')
        else:
            self.tenant_id = tenant_id
        
        
        # client_secret
        if client_secret is None:
            
            if Configurations['Azure.SP.client_secret'] is None:
                
                if os.getenv('AZURE_CLIENT_SECRET') is None:
                    
                    client_secret = getpass('Client secret: ')
                    
                else:
                    print('Client secret was retrieved from AZURE_CLIENT_SECRET environmental variable')
                    client_secret = os.getenv('AZURE_CLIENT_SECRET')
            else:
                client_secret = Configurations['Azure.SP.client_secret']
                
                
        if client_secret is None:
            raise ValueError('Client secret needs to be provided')
        else:
            self.client_secret = client_secret
            
        self = super().__init__(client_id= self.client_id, tenant_id= self.tenant_id, client_secret = self.client_secret)


class KeyVaultclient(SecretClient):
    
    
    def __init__(self, vault_url, credential = None):
        
        '''
        
        Parameters:
        
            vault_url (str) – RL of the vault the client will access. This is also called the vault's "DNS Name".
            credential (str) –  An object which can provide an access token for the vault, such as a service principal credential
            
        Example:
        
        .. code-block:: python
            
            import pynomial as pyn
            
            client = pyn.KeyVaultclient(vault_url='https://keyvaulttestinstance.vault.azure.net/')
            retrieved_secret = client.get_secret('MyPassword')
            retrieved_secret.value


        .. code-block:: python
            
            import pynomial as pyn

            credential = pyn.SPCredential()
            client = pyn.KeyVaultclient(vault_url='https://keyvaulttestinstance.vault.azure.net/', credential=credential)
            retrieved_secret = client.get_secret('MyPassword').value
            
        '''
        from azure.identity import InteractiveBrowserCredential

        if credential is None:
            credential = InteractiveBrowserCredential()
            self.token = credential.get_token()
            
            
        self = super().__init__(vault_url = vault_url, credential=credential)